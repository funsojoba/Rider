from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.user_type == "ADMIN"


class IsUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return user.user_type == "USER"


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.user_type == "SUPER_ADMIN"


class IsRider(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.user_type == "RIDER"
