from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'price',
            'description',
            'stock',
            'category',
        ]
        labels = {
            'title': _('Title'),
            'author': _('Author'),
            'price': _('Price'),
            'description': _('Description'),
            'stock': _('Stock'),
            'category': _('Category'),
        }