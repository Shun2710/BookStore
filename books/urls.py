from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    cart_add,
    cart_remove,
    cart_clear,
    cart_detail,
    create_checkout_session,
    create_order,
)


app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/add/', BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('cart/add/<int:book_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:book_id>/', cart_remove, name='cart_remove'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('cart/', cart_detail, name='cart_detail'),
    path('checkout/', create_checkout_session, name='create_checkout_session'),
    path('order/create/', create_order, name='create_order'),
]