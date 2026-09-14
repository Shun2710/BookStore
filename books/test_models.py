import pytest

from books.factories import (
    BookFactory,
    CategoryFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_category_str():
    category = CategoryFactory(name="Fiction")
    assert str(category) == "Fiction"


@pytest.mark.django_db
def test_book_str():
    book = BookFactory(title="1984")
    assert str(book) == "1984"


@pytest.mark.django_db
def test_book_has_category():
    category = CategoryFactory(name="Classics")
    book = BookFactory(category=category)

    assert book.category == category


@pytest.mark.django_db
def test_book_default_stock():
    book = BookFactory(stock=10)
    assert book.stock == 10


@pytest.mark.django_db
def test_order_str():
    order = OrderFactory()
    assert str(order) == f"Order #{order.id}"


@pytest.mark.django_db
def test_order_item_str():
    item = OrderItemFactory(quantity=3)

    assert str(item) == f"3 x {item.book.title}"


@pytest.mark.django_db
def test_order_item_price_matches_book():
    item = OrderItemFactory()

    assert item.price == item.book.price


@pytest.mark.django_db
def test_order_contains_items():
    order = OrderFactory()
    item = OrderItemFactory(order=order)

    assert item in order.items.all()