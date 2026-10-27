from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from .models import Stock


class StockAPITest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.stock = Stock.objects.create(book_id=1, quantity=10)

    def test_get_stocks(self):
        response = self.client.get("/api/stocks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["quantity"], 10)

    def test_filter_by_book_id(self):
        response = self.client.get("/api/stocks/?book_id=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_stock(self):
        self.user.is_staff = True
        self.user.save()

        response = self.client.post(
            "/api/stocks/",
            {"book_id": 2, "quantity": 5},
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Stock.objects.filter(book_id=2).exists())

    def test_unauthorized_access(self):
        client = APIClient()
        response = client.get("/api/stocks/")
        self.assertIn(response.status_code, [401, 403])

    def test_regular_user_cannot_create_stock(self):
        response = self.client.post(
            "/api/stocks/",
            {"book_id": 3, "quantity": 7},
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Stock.objects.filter(book_id=3).exists())

    def test_regular_user_cannot_create_stock(self):
        response = self.client.post(
            "/api/stocks/",
            {"book_id": 3, "quantity": 7},
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Stock.objects.filter(book_id=3).exists())
