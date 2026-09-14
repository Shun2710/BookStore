import pytest
from django.urls import reverse

from books.factories import BookFactory, CategoryFactory


@pytest.mark.django_db
def test_book_list_view_returns_200(client):
    response = client.get(reverse("books:book_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_book_detail_view_returns_200(client):
    book = BookFactory()

    response = client.get(
        reverse("books:book_detail", args=[book.pk])
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_list_filter_by_category(client):
    category = CategoryFactory(slug="fiction")
    book = BookFactory(category=category)

    response = client.get(
        reverse("books:book_list"),
        {"category": "fiction"},
    )

    assert response.status_code == 200
    assert book.title.encode() in response.content


@pytest.mark.django_db
def test_async_book_count(client):
    BookFactory.create_batch(3)

    response = client.get(
        reverse("books:async_book_count")
    )

    assert response.status_code == 200
    assert response.json()["book_count"] == 3


@pytest.mark.django_db
def test_async_book_detail(client):
    book = BookFactory(
        title="Async Book",
        author="Async Author",
    )

    response = client.get(
        reverse(
            "books:async_book_detail",
            args=[book.pk],
        )
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == book.id
    assert data["title"] == "Async Book"
    assert data["author"] == "Async Author"


@pytest.mark.django_db
def test_async_book_list(client):
    BookFactory(title="Book A")
    BookFactory(title="Book B")

    response = client.get(
        reverse("books:async_book_list")
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data["books"]) == 2