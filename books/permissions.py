from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAdminUser,
)


class IsAdminOrReadOnly(IsAdminUser):
    """Allow read access to everyone and write access only to admin users."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request, view)

        if hasattr(obj, "user"):
            return obj.user == request.user

        if hasattr(obj, "owner"):
            return obj.owner == request.user

        return False

from rest_framework.permissions import IsAdminUser


class IsAdminOrReadOnly(IsAdminUser):
    """Allow read access to everyone and write access only to admin users."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return super().has_permission(request, view)