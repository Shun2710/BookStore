import stripe

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.db import transaction
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Book, Category, Order, OrderItem
from .forms import BookForm
from .cart import Cart


async def async_book_count(request):
    """Return the total number of books using an asynchronous database query."""
    book_count = await Book.objects.acount()

    return JsonResponse({
        "book_count": book_count,
    })

async def async_book_detail(request, book_id):
    """Return details of a single book using an asynchronous database query."""
    book = await Book.objects.aget(pk=book_id)

    return JsonResponse({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": str(book.price),
        "stock": book.stock,
    })

async def async_book_list(request):
    """Return all books as JSON using asynchronous queryset iteration."""
    books = []

    async for book in Book.objects.all().order_by("title"):
        books.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": str(book.price),
            "stock": book.stock,
        })

    return JsonResponse({
        "books": books,
    })

class BookListView(ListView):
    """Display a paginated list of books with search and category filtering."""

    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 5
    ordering = ['title']

    def get_queryset(self):
        queryset = Book.objects.all().order_by('title')

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search)
            )

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_category = self.request.GET.get("category", "")
        categories = Category.objects.all()

        context["category_options"] = [
            {
                "category": category,
                "selected": (
                    "selected"
                    if category.slug == selected_category
                    else ""
                ),
           }
           for category in categories
        ]

        return context



class BookDetailView(DetailView):
    """Display detailed information about a single book."""

    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'


class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Allow staff users to create a new book."""

    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')

    def test_func(self):
        return self.request.user.is_staff


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow staff users to update an existing book."""

    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')

    def test_func(self):
        return self.request.user.is_staff


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow staff users to delete an existing book."""

    model = Book
    template_name = 'books/book_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff
    success_url = reverse_lazy('books:book_list')


def cart_add(request, book_id):
    """Add the selected book to the shopping cart."""

    cart = Cart(request)
    book = Book.objects.get(id=book_id)
    cart.add(book=book)
    return redirect('books:cart_detail')


def cart_remove(request, book_id):
    """Remove the selected book from the shopping cart."""

    cart = Cart(request)
    book = Book.objects.get(id=book_id)
    cart.remove(book)
    return redirect('books:book_list')


def cart_clear(request):
    """Remove all books from the shopping cart."""

    cart = Cart(request)
    cart.clear()
    return redirect('books:book_list')


def create_checkout_session(request):
    """Create a Stripe Checkout Session for the books in the shopping cart."""

    stripe.api_key = settings.STRIPE_SECRET_KEY
    cart = Cart(request)

    if not cart.cart:
        return redirect("books:cart_detail")

    book_ids = cart.cart.keys()
    books = Book.objects.in_bulk(book_ids)

    line_items = []

    for book_id, item in cart.cart.items():
        book = books.get(int(book_id))

        if book is None:
            continue

        line_items.append({
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": book.title,
                },
                "unit_amount": int(book.price * 100),
            },
            "quantity": item["quantity"],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("books:create_order")
        ),
        cancel_url=request.build_absolute_uri(
            reverse("books:book_list")
        ),
    )

    return redirect(session.url)

def create_order(request):
    """Create an order from the cart and send a confirmation email after commit."""

    cart = Cart(request)

    with transaction.atomic():
        order = Order.objects.create()

        for book_id, item in cart.cart.items():
            book = Book.objects.get(id=book_id)

            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=item["quantity"],
                price=book.price,
            )

        transaction.on_commit(
            lambda: send_mail(
                subject="Order created",
                message=(
                    f"Your order #{order.id} "
                    "has been created successfully."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        )

    cart.clear()

    return redirect("books:book_list")

    send_mail(
    subject="Order created",
    message=f"Your order #{order.id} has been created successfully.",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[settings.DEFAULT_FROM_EMAIL],
    fail_silently=False,
    )

    
    return redirect("books:book_list")


def cart_detail(request):
    """Display the current contents of the shopping cart."""

    cart = Cart(request)
    return render(request, "books/cart_detail.html", {"cart": cart})