from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    """."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_staff and request.user.is_superuser)

    # def has_object_permission(self, request, view, obj):
    #     print(obj, view, request)
    #     return True
        # return bool((request.method in permissions.SAFE_METHODS)
        #             or (obj.author == request.user)
        #             or (request.user.role in (Roles.ADMIN, Roles.MODERATOR, )))
