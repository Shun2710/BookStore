import pytest
from rest_framework import status
from rest_framework.test import APIClient

from .factories import BookFactory, CategoryFactory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_books_list(api_client):
    BookFactory.create_batch(3)

    response = api_client.get("/api/books/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3


@pytest.mark.django_db
def test_book_detail(api_client):
    book = BookFactory()

    response = api_client.get(f"/api/books/{book.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == book.id
    assert response.data["title"] == book.title


@pytest.mark.django_db
def test_books_filter_by_author(api_client):
    BookFactory(author="Test Author")
    BookFactory(author="Other Author")

    response = api_client.get("/api/books/", {"author": "Test Author"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["author"] == "Test Author"


@pytest.mark.django_db
def test_anonymous_user_cannot_create_book(api_client):
    book = BookFactory.build()

    data = {
        "title": book.title,
        "author": book.author,
        "price": str(book.price),
        "description": book.description,
        "stock": book.stock,
    }

    response = api_client.post("/api/books/", data, format="json")

    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


@pytest.mark.django_db
def test_admin_can_create_book(api_client):
    admin = UserFactory(is_staff=True, is_superuser=True)
    api_client.force_authenticate(user=admin)

    category = CategoryFactory()

    data = {
        "title": "API Test Book",
        "author": "API Author",
        "price": "19.99",
        "description": "Created through the REST API",
        "stock": 5,
        "category_id": category.id,
    }

    response = api_client.post("/api/books/", data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "API Test Book"

@pytest.mark.django_db
def test_categories_list(api_client):
    CategoryFactory.create_batch(3)

    response = api_client.get("/api/categories/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3


@pytest.mark.django_db
def test_category_detail(api_client):
    category = CategoryFactory()

    response = api_client.get(f"/api/categories/{category.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == category.id
    assert response.data["name"] == category.name


@pytest.mark.django_db
def test_categories_filter_by_slug(api_client):
    category = CategoryFactory(name="Fantasy", slug="fantasy")
    CategoryFactory(name="History", slug="history")

    response = api_client.get(
        "/api/categories/",
        {"slug": category.slug},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["slug"] == "fantasy"


@pytest.mark.django_db
def test_anonymous_user_cannot_create_category(api_client):
    data = {
        "name": "Science Fiction",
        "slug": "science-fiction",
    }

    response = api_client.post(
        "/api/categories/",
        data,
        format="json",
    )

    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


@pytest.mark.django_db
def test_admin_can_create_category(api_client):
    admin = UserFactory(is_staff=True, is_superuser=True)
    api_client.force_authenticate(user=admin)

    data = {
        "name": "Science Fiction",
        "slug": "science-fiction",
    }

    response = api_client.post(
        "/api/categories/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Science Fiction"
    assert response.data["slug"] == "science-fiction"

@pytest.mark.django_db
def test_anonymous_user_cannot_view_orders(api_client):
    response = api_client.get("/api/orders/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_authenticated_user_can_view_orders(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)

    response = api_client.get("/api/orders/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_orders_list_contains_created_order(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)

    from .factories import OrderFactory

    order = OrderFactory()

    response = api_client.get("/api/orders/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == order.id


@pytest.mark.django_db
def test_order_detail(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)

    from .factories import OrderFactory

    order = OrderFactory()

    response = api_client.get(f"/api/orders/{order.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == order.id
    assert "items" in response.data


@pytest.mark.django_db
def test_order_contains_nested_items(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)

    from .factories import OrderItemFactory

    order_item = OrderItemFactory()

    response = api_client.get(
        f"/api/orders/{order_item.order.id}/"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["items"]) == 1
    assert response.data["items"][0]["quantity"] == order_item.quantity
    assert "book" in response.data["items"][0]

@pytest.mark.django_db
def test_anonymous_user_cannot_view_cart(api_client):
    response = api_client.get("/api/cart/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_authenticated_user_can_view_empty_cart(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)

    response = api_client.get("/api/cart/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_authenticated_user_can_add_book_to_cart(api_client):
    user = UserFactory()
    book = BookFactory()
    api_client.force_authenticate(user=user)

    response = api_client.post(
        "/api/cart/add/",
        {
            "book_id": book.id,
            "quantity": 2,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == "Book added to cart."


@pytest.mark.django_db
def test_cart_contains_added_book(api_client):
    user = UserFactory()
    book = BookFactory()
    api_client.force_authenticate(user=user)

    api_client.post(
        "/api/cart/add/",
        {
            "book_id": book.id,
            "quantity": 2,
        },
        format="json",
    )

    response = api_client.get("/api/cart/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["book_id"] == book.id
    assert response.data[0]["quantity"] == 2


@pytest.mark.django_db
def test_authenticated_user_can_remove_book_from_cart(api_client):
    user = UserFactory()
    book = BookFactory()
    api_client.force_authenticate(user=user)

    api_client.post(
        "/api/cart/add/",
        {
            "book_id": book.id,
            "quantity": 1,
        },
        format="json",
    )

    response = api_client.post(
        "/api/cart/remove/",
        {
            "book_id": book.id,
            "quantity": 1,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    cart_response = api_client.get("/api/cart/")
    assert cart_response.data == []

@pytest.mark.django_db
def test_jwt_token_obtain(api_client):
    user = UserFactory()
    user.set_password("testpass123")
    user.save()

    response = api_client.post(
        "/api/token/",
        {
            "username": user.username,
            "password": "testpass123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_jwt_token_invalid_credentials(api_client):
    user = UserFactory()
    user.set_password("testpass123")
    user.save()

    response = api_client.post(
        "/api/token/",
        {
            "username": user.username,
            "password": "wrong-password",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_jwt_token_refresh(api_client):
    user = UserFactory()
    user.set_password("testpass123")
    user.save()

    token_response = api_client.post(
        "/api/token/",
        {
            "username": user.username,
            "password": "testpass123",
        },
        format="json",
    )

    response = api_client.post(
        "/api/token/refresh/",
        {
            "refresh": token_response.data["refresh"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_jwt_token_verify(api_client):
    user = UserFactory()
    user.set_password("testpass123")
    user.save()

    token_response = api_client.post(
        "/api/token/",
        {
            "username": user.username,
            "password": "testpass123",
        },
        format="json",
    )

    response = api_client.post(
        "/api/token/verify/",
        {
            "token": token_response.data["access"],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_jwt_access_token_can_access_orders(api_client):
    user = UserFactory()
    user.set_password("testpass123")
    user.save()

    token_response = api_client.post(
        "/api/token/",
        {
            "username": user.username,
            "password": "testpass123",
        },
        format="json",
    )

    access_token = token_response.data["access"]

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    response = api_client.get("/api/orders/")

    assert response.status_code == status.HTTP_200_OK