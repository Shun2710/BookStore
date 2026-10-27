from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("book_id", "quantity", "updated_at")
    search_fields = ("book_id",)
