from django.utils.translation import gettext_lazy as _
from django.db import models

class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    author = models.CharField(_("Author"), max_length=255)
    price = models.DecimalField(
        _("Price"),
        max_digits=8,
        decimal_places=2
    )
    description = models.TextField(_("Description"), blank=True)
    stock = models.PositiveIntegerField(_("Stock"), default=0)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name=_("Category"),
    )

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title
    
class Order(models.Model):
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Order"),
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name=_("Book"),
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=1
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=8,
        decimal_places=2
    )

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"