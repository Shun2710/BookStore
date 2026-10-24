from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Stock
from .serializers import StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Stock.objects.all()
        book_id = self.request.query_params.get("book_id")

        if book_id is not None:
            queryset = queryset.filter(book_id=book_id)

        return queryset