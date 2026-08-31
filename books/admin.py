from django.contrib import admin
from .models import Book, Category, Order, OrderItem


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "stock", "category")
    list_filter = ("category", "author")
    search_fields = ("title", "author")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    inlines = [OrderItemInline]