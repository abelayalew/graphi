from rest_framework.permissions import BasePermission

from accounts.choices import UserTypeChoice


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsCybermindsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return (
            request.user.user_type == UserTypeChoice.CYBER_ADMIN
            or request.user.is_superuser
        )


class IsClientAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return request.user.user_type == UserTypeChoice.CLIENT_ADMIN


class IsClientUser(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return request.user.user_type == UserTypeChoice.CLIENT_USER


class IsClient(BasePermission):
    """
    either client or client admin has permission
    """

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return (
            request.user.user_type == UserTypeChoice.CLIENT_USER
            or request.user.user_type == UserTypeChoice.CLIENT_ADMIN
        )
