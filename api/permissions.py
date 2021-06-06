from rest_framework import permissions

from user.models import Profile


class CustomPermission(permissions.BasePermission):
    """."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            (request.user.is_staff and request.user.is_superuser)
            or (request.user.profile)
        )

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        profile = Profile.objects.filter(user=request.user)[0]
        print(request.user, profile in obj.profiles.all())
        if (
                request.method in permissions.SAFE_METHODS
                or profile in obj.profiles.all()
        ):
            return True
        return False
        # return bool((request.method in permissions.SAFE_METHODS)
        #             or (obj.author == request.user)
        #             or (request.user.role in (Roles.ADMIN, Roles.MODERATOR, )))
