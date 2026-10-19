from django.db.models import Sum

from .models import Book, Order, OrderItem
from celery import shared_task
from django.core.mail import send_mail
from django.core.management import call_command


@shared_task
def send_order_email(subject, message, recipient_email):
    """Send an order confirmation email in the background."""
    return send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[recipient_email],
        fail_silently=False,
    )


@shared_task
def generate_bookstore_report():
    """Generate a summary report about books and orders."""
    return {
        "total_books": Book.objects.count(),
        "total_orders": Order.objects.count(),
        "total_items_sold": (
            OrderItem.objects.aggregate(total=Sum("quantity"))["total"] or 0
        ),
    }


@shared_task
def cleanup_expired_sessions():
    """Remove expired Django sessions."""
    call_command("clearsessions")
    return "Expired sessions cleaned successfully."
