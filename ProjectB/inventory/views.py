from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Stock
from .serializers import StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Stock.objects.all()
        book_id = self.request.query_params.get("book_id")

        if book_id is not None:
            queryset = queryset.filter(book_id=book_id)

        return queryset