from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Book


@receiver([post_save, post_delete], sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    """Clear cached book details after saving or deleting a book."""
    cache.delete(f"book_detail_{instance.pk}")
