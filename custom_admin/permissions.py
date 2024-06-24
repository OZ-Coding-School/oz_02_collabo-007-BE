from rest_framework.permissions import BasePermission

from club.models import Club


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsCoach(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsClubCoach(BasePermission):
    def has_object_permission(self, request, view, club: Club):
        return bool(request.user and request.user.is_admin) or club.coaches.filter(user=request.user).exists()
