import stripe

from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.db import transaction
from django.core.mail import send_mail
from django.urls import reverse_lazy
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


class BookListView(ListView):
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

        selected_category = self.request.GET.get('category', '')
        categories = Category.objects.all()

        context['category_options'] = [
        {
            'category': category,
            'selected': 'selected' if category.slug == selected_category else ''
        }
        for category in categories
    ]

        return context



class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'


class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')

    def test_func(self):
        return self.request.user.is_staff


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')

    def test_func(self):
        return self.request.user.is_staff


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_staff
    success_url = reverse_lazy('books:book_list')


def cart_add(request, book_id):
    cart = Cart(request)
    book = Book.objects.get(id=book_id)
    cart.add(book=book)
    return redirect('books:cart_detail')


def cart_remove(request, book_id):
    cart = Cart(request)
    book = Book.objects.get(id=book_id)
    cart.remove(book)
    return redirect('books:book_list')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('books:book_list')


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    cart = Cart(request)
    line_items = []

    for book_id, item in cart.cart.items():
        book = Book.objects.get(id=book_id)

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
        success_url=request.build_absolute_uri("/order/create/"),
        cancel_url=request.build_absolute_uri("/"),
    )

    return redirect(session.url)

def create_order(request):
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

    cart.clear()


    send_mail(
    subject="Order created",
    message=f"Your order #{order.id} has been created successfully.",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[settings.DEFAULT_FROM_EMAIL],
    fail_silently=False,
    )

    
    return redirect("books:book_list")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "books/cart_detail.html", {"cart": cart})