from rest_framework import permissions

from pharmacy_app.models import Staff


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

    from rest_framework import permissions

class IsWarehouseOrAdmin(permissions.BasePermission):
    """
    Custom permission:
    - Warehouse role and Admin role can create & delete product.
    - Authenticated user can retrieve product.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in ["POST", "DELETE"]:
            return request.user.is_staff or request.user.role == Staff.StaffRoleChoices.WAREHOUSE

        if request.method in ["GET"]:
            return request.user.is_authenticated

        return False