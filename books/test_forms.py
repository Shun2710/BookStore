import pytest

from books.forms import BookForm
from books.factories import CategoryFactory


@pytest.mark.django_db
def test_book_form_valid():
    category = CategoryFactory()

    form = BookForm(data={
        "title": "Dune",
        "author": "Frank Herbert",
        "price": "19.99",
        "description": "Science fiction novel",
        "stock": 5,
        "category": category.id,
    })

    assert form.is_valid()


@pytest.mark.django_db
def test_book_form_title_required():
    category = CategoryFactory()

    form = BookForm(data={
        "title": "",
        "author": "Author",
        "price": "10.00",
        "description": "",
        "stock": 1,
        "category": category.id,
    })

    assert not form.is_valid()
    assert "title" in form.errors


@pytest.mark.django_db
def test_book_form_author_required():
    category = CategoryFactory()

    form = BookForm(data={
        "title": "Book",
        "author": "",
        "price": "10.00",
        "description": "",
        "stock": 1,
        "category": category.id,
    })

    assert not form.is_valid()
    assert "author" in form.errors


@pytest.mark.django_db
def test_book_form_price_required():
    category = CategoryFactory()

    form = BookForm(data={
        "title": "Book",
        "author": "Author",
        "price": "",
        "description": "",
        "stock": 1,
        "category": category.id,
    })

    assert not form.is_valid()
    assert "price" in form.errors


@pytest.mark.django_db
def test_book_form_stock_cannot_be_negative():
    category = CategoryFactory()

    form = BookForm(data={
        "title": "Book",
        "author": "Author",
        "price": "10.00",
        "description": "",
        "stock": -1,
        "category": category.id,
    })

    assert not form.is_valid()
    assert "stock" in form.errors


@pytest.mark.django_db
def test_book_form_category_required():
    form = BookForm(data={
        "title": "Book",
        "author": "Author",
        "price": "10.00",
        "description": "",
        "stock": 1,
        "category": "",
    })

    assert not form.is_valid()
    assert "category" in form.errors