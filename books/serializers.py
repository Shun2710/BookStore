from rest_framework import serializers

from .models import Book, Category, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for book categories."""

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BookSerializer(serializers.ModelSerializer):
    """Serializer for books with nested category data."""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "price",
            "description",
            "stock",
            "category",
            "category_id",
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for items contained in an order."""

    book = BookSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "book",
            "quantity",
            "price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders with nested order items."""

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "items",
        ]

class CartItemSerializer(serializers.Serializer):
    """Serializer for an item stored in the shopping cart."""

    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
        read_only=True,
    )


class CartAddSerializer(serializers.Serializer):
    """Serializer for adding a book to the shopping cart."""

    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(
        min_value=1,
        default=1,
    )