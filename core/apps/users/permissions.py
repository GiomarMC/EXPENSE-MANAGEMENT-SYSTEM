from rest_framework.permissions import BasePermission
from apps.users.constants import Roles


class HasStoreRole(BasePermission):
    allow_roles = []

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if not self.allow_roles:
            return True

        return user.tiendas.filter(
            rol__nombre__in=self.allow_roles
        ).exists()


class IsOwnerOnly(HasStoreRole):
    allow_roles = [Roles.DUENO]


class IsAdminOrOwner(HasStoreRole):
    allow_roles = [Roles.ADMIN, Roles.DUENO]


class IsWorkerOrAdminOrOwner(HasStoreRole):
    allow_roles = [Roles.TRABAJADOR, Roles.ADMIN, Roles.DUENO]
