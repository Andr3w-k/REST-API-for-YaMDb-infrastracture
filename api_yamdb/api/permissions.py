"""api_permissions."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModeratorOrAdminOrAuthor(BasePermission):
    """IsModeratorOrAdminOrAuthor."""
    def has_object_permission(self, request, view, obj):
        """IsModeratorOrAdminOrAuthor_has_object_permission."""
        return (request.method in SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_moderator
                or request.user.is_admin
                or obj.author == request.user)


class IsAdmin(BasePermission):
    """IsAdmin."""
    def has_permission(self, request, view):
        """IsAdmin_has_permission."""
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    """IsAdminOrReadOnly."""
    def has_permission(self, request, view):
        """IsAdminOrReadOnly_has_permission."""
        return (request.method in SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_authenticated
                and request.user.is_admin
                )
