from rest_framework.routers import DefaultRouter

from .views import BookViewSet, CategoryViewSet


router = DefaultRouter()
router.register("books", BookViewSet, basename="api-books")
router.register("categories", CategoryViewSet, basename="api-categories")


urlpatterns = router.urls