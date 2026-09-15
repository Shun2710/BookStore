# AI Code Review — BookStore

## Overview

This document describes an AI-assisted code review performed for three parts of the BookStore Django project.

The following components were reviewed:

1. `BookListView`
2. `create_checkout_session`
3. `create_order`

The AI recommendations were reviewed before being applied. Only recommendations considered appropriate for the current project were implemented.

---

# 1. BookListView

## Original Code

```python
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
```

## AI Review

The filtering logic in `get_queryset()` is appropriate for the current project and does not require a major rewrite.

AI recommendations:

- Keep the existing lazy Django QuerySet filtering.
- Improve formatting and readability of `get_context_data()`.
- Use consistent quote style.
- Make the conditional expression for the selected category easier to read.
- Avoid unnecessary changes to working query logic.

## Applied Changes

The existing search and category filtering logic was preserved.

The construction of `category_options` was reformatted to improve readability and maintainability.

## Final Code

```python
class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 5
    ordering = ["title"]

    def get_queryset(self):
        queryset = Book.objects.all().order_by("title")

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(author__icontains=search)
            )

        category = self.request.GET.get("category")
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
```

## Verification

The relevant view tests were executed after the review.

Result:

```text
2 passed
```

---

# 2. create_checkout_session

## Original Code

```python
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
```

## AI Review

AI identified several potential improvements:

- Avoid calling `Book.objects.get()` once for every cart item.
- Fetch the required books in a single database query.
- Handle an empty cart before contacting Stripe.
- Avoid hard-coded application URLs.
- Use Django URL reversing for success and cancellation URLs.
- Keep the Stripe API call isolated from database preparation logic.

## Applied Changes

The following recommendations were applied:

- `Book.objects.in_bulk()` is used to retrieve books efficiently.
- Empty carts redirect back to the cart page.
- `reverse()` is used instead of hard-coded paths.
- Missing books are skipped safely while preparing Stripe line items.

## Final Code

```python
def create_checkout_session(request):
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
```

## Verification

The Stripe integration test uses a mocked Stripe Checkout Session, so no real payment request is performed.

Result:

```text
1 passed
```

---

# 3. create_order

## Original Code

```python
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
```

## AI Review

The use of `transaction.atomic()` for creating an order and its items is appropriate.

However, the email was sent independently after the transaction block.

AI recommendations:

- Keep order and order-item creation atomic.
- Send the notification only after the database transaction has committed successfully.
- Use `transaction.on_commit()` for the email side effect.
- Clear the cart after successful order creation.
- Keep external side effects separate from the database transaction.

## Applied Changes

Email delivery was registered with `transaction.on_commit()`.

This ensures that the email is not scheduled when the database transaction fails and rolls back.

The cart continues to be cleared after successful order creation.

## Final Code

```python
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
```

## Verification

The existing order integration test was executed after applying the recommendation.

Result:

```text
1 passed
```

---

# AI Review Summary

The AI review focused on maintainability, database efficiency, transaction safety, and avoiding hard-coded URLs.

Recommendations were not applied automatically. They were reviewed first and then tested against the existing project.

Main improvements:

- Reduced repeated database queries during Stripe Checkout preparation.
- Added empty-cart handling before Stripe Checkout.
- Replaced hard-coded URLs with Django `reverse()`.
- Improved transaction handling for order notification email.
- Improved readability of `BookListView`.
- Verified all modified functionality with automated tests.

The reviewed code remained compatible with the existing BookStore functionality.