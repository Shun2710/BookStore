import pytest
from django.urls import reverse

from books.factories import BookFactory


@pytest.mark.django_db
def test_create_checkout_session_uses_stripe_mock(client, monkeypatch):
    book = BookFactory(price="15.99")

    client.get(
        reverse("books:cart_add", args=[book.pk])
    )

    class FakeSession:
        url = "https://stripe.test/checkout"

    def fake_create(**kwargs):
        return FakeSession()

    monkeypatch.setattr(
        "books.views.stripe.checkout.Session.create",
        fake_create,
    )

    response = client.get(
        reverse("books:create_checkout_session")
    )

    assert response.status_code == 302
    assert response.url == "https://stripe.test/checkout"