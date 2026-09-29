from rest_framework.routers import DefaultRouter

from .views import BookViewSet, CartViewSet, CategoryViewSet, OrderViewSet


router = DefaultRouter()


router.register("books", BookViewSet, basename="api-books")
router.register("categories", CategoryViewSet, basename="api-categories")
router.register("orders", OrderViewSet, basename="api-orders")
router.register("cart", CartViewSet, basename="api-cart")

urlpatterns = router.urls