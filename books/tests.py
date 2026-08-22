from django.test import TestCase
from .models import Book, Category


class BookModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Fiction",
            slug="fiction"
        )

        self.book = Book.objects.create(
            title="1984",
            author="George Orwell",
            price=12.99,
            description="Dystopian novel",
            stock=5,
            category=self.category
        )

    def test_book_created(self):
        self.assertEqual(self.book.title, "1984")
        self.assertEqual(self.book.author, "George Orwell")
        self.assertEqual(self.book.stock, 5)
        self.assertEqual(self.book.category.name, "Fiction")

    def test_book_string(self):
        self.assertEqual(str(self.book), "1984")

class BookViewTest(TestCase):

    def test_book_list_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_book_detail_page(self):
        category = Category.objects.create(name="Fiction", slug="fiction")
        book = Book.objects.create(
            title="1984",
            author="George Orwell",
            price=12.99,
            stock=5,
            category=category
        )

        response = self.client.get(f"/book/{book.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1984")


    def test_filter_by_category(self):
        category = Category.objects.create(name="Fiction", slug="fiction")
        Book.objects.create(
            title="1984",
            author="George Orwell",
            price=12.99,
            stock=5,
            category=category
       )

        response = self.client.get("/?category=fiction")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1984") 