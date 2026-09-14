import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from books.factories import (
    UserFactory,
    BookFactory,
    CategoryFactory,
)
from books.models import Order


User = get_user_model()


@pytest.mark.django_db
def test_home_page_loads(client):
    response = client.get(reverse("books:book_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_book_detail_flow(client):
    book = BookFactory()

    response = client.get(
        reverse("books:book_detail", args=[book.pk])
    )

    assert response.status_code == 200
    assert book.title.encode() in response.content


@pytest.mark.django_db
def test_search_by_title(client):
    book = BookFactory(title="Dune")

    response = client.get(
        reverse("books:book_list"),
        {"search": "Dune"},
    )

    assert response.status_code == 200
    assert b"Dune" in response.content


@pytest.mark.django_db
def test_search_by_author(client):
    book = BookFactory(author="George Orwell")

    response = client.get(
        reverse("books:book_list"),
        {"search": "George Orwell"},
    )

    assert response.status_code == 200
    assert b"George Orwell" in response.content


@pytest.mark.django_db
def test_filter_by_category(client):
    category = CategoryFactory(slug="fiction")
    book = BookFactory(category=category)

    response = client.get(
        reverse("books:book_list"),
        {"category": "fiction"},
    )

    assert response.status_code == 200
    assert book.title.encode() in response.content


@pytest.mark.django_db
def test_user_can_register(client):
    response = client.post(
        reverse("register"),
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        },
    )

    assert response.status_code in (200, 302)
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_user_can_login(client):
    user = UserFactory(username="loginuser")
    user.set_password("StrongPass123!")
    user.save()

    logged_in = client.login(
        username="loginuser",
        password="StrongPass123!",
    )

    assert logged_in is True


@pytest.mark.django_db
def test_authenticated_user_can_view_books(client):
    user = UserFactory()
    client.force_login(user)

    response = client.get(reverse("books:book_list"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_staff_can_open_add_book_page(client):
    user = UserFactory(is_staff=True)
    client.force_login(user)

    response = client.get(reverse("books:book_create"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_regular_user_cannot_open_add_book_page(client):
    user = UserFactory(is_staff=False)
    client.force_login(user)

    response = client.get(reverse("books:book_create"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_add_book_to_cart_flow(client):
    book = BookFactory()

    response = client.get(
        reverse("books:cart_add", args=[book.pk])
    )

    assert response.status_code == 302
    assert "cart" in client.session
    assert str(book.pk) in client.session["cart"]


@pytest.mark.django_db
def test_remove_book_from_cart_flow(client):
    book = BookFactory()

    client.get(
        reverse("books:cart_add", args=[book.pk])
    )

    response = client.get(
        reverse("books:cart_remove", args=[book.pk])
    )

    assert response.status_code == 302
    assert str(book.pk) not in client.session["cart"]


@pytest.mark.django_db
def test_clear_cart_flow(client):
    book = BookFactory()

    client.get(
        reverse("books:cart_add", args=[book.pk])
    )

    response = client.get(
        reverse("books:cart_clear")
    )

    assert response.status_code == 302
    assert client.session["cart"] == {}


@pytest.mark.django_db
def test_cart_page_flow(client):
    book = BookFactory()

    client.get(
        reverse("books:cart_add", args=[book.pk])
    )

    response = client.get(
        reverse("books:cart_detail")
    )

    assert response.status_code == 200
    assert str(book.pk).encode() in response.content


@pytest.mark.django_db
def test_create_order_flow(client, monkeypatch):
    book = BookFactory()

    client.get(
        reverse("books:cart_add", args=[book.pk])
    )

    monkeypatch.setattr(
        "books.views.send_mail",
        lambda *args, **kwargs: 1,
    )

    response = client.get(
        reverse("books:create_order")
    )

    assert response.status_code == 302
    assert Order.objects.count() == 1
    assert Order.objects.first().items.count() == 1