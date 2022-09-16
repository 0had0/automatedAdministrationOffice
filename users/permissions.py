from rest_framework import permissions


class IsDirector(permissions.BasePermission):
    message = 'You must be a Director!'

    def has_permission(self, request, view):
        return request.user.is_director
