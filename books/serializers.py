from rest_framework import serializers

from .models import Book, Category


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