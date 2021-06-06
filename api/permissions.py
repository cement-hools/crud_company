from rest_framework import permissions

from user.models import Roles


class CompanyPermission(permissions.BasePermission):
    """."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            (request.user.is_staff and request.user.is_superuser)
            or (
                    request.user.is_authenticated and
                    request.user.profile.role == Roles.MODERATOR
            )
        )

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True
        profile = request.user.profile
        if (
                (
                        request.method in permissions.SAFE_METHODS
                        and profile in obj.profiles.all()
                ) or
                (profile in obj.profiles.all() and
                 profile.role == Roles.MODERATOR)
        ):
            return True
        return False


class NewsPermission(permissions.BasePermission):
    """."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or
                (
                        request.user.profile.role == Roles.MODERATOR
                        and obj.company == request.user.profile.company
                )
        ):
            return True
        return False
