from rest_framework.permissions import BasePermission
from apps.users.constants import Roles


class IsAuthenticatedAndHasRole(BasePermission):
    allow_roles = []

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.tiendas.filter(
            rol__nombre__in=self.allow_roles
        ).exists()


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsAdmin(IsAuthenticatedAndHasRole):
    allow_roles = [Roles.ADMIN]


class IsWorker(IsAuthenticatedAndHasRole):
    allow_roles = [Roles.TRABAJADOR]


class CanViewEarnings(IsAuthenticatedAndHasRole):
    allow_roles = [Roles.ADMIN]


class IsAdminOfStore(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.tiendas.filter(
            tienda=obj.tienda,
            rol__nombre=Roles.ADMIN
        ).exists()
