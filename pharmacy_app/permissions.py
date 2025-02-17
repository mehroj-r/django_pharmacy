from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission:
    - Users can retrieve & update their own data.
    - Only admins can delete users.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in ["GET", "POST"]:
            return obj == request.user or request.user.is_staff  # Owners & admins can update

        if request.method in ["DELETE"]:
            return request.user.is_staff  # Only admins can delete

        return False