from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books"
    )

class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

def __str__(self):
        return self.title
    
class Order(models.Model): 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
        order = models.ForeignKey( Order,
        on_delete=models.CASCADE,
        related_name="items"
        )
        book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
        )
        quantity = models.PositiveIntegerField(default=1)
        price = models.DecimalField(max_digits=8, decimal_places=2)

        def __str__(self):
            return f"{self.quantity} x {self.book.title}"