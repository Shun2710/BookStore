from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAdminUser,
)


class IsOwnerOrReadOnly(BasePermission):
    """Allow read access to everyone and editing only to the owner."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, "user"):
            return obj.user == request.user

        if hasattr(obj, "owner"):
            return obj.owner == request.user

        return False


class IsAdminOrReadOnly(IsAdminUser):
    """Allow read access to everyone and write access only to admin users."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request, view)
