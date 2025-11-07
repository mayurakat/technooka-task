from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "LIBRARIAN"


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            obj.user == request.user
        )
