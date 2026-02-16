from rest_framework import viewsets
from apps.users.models import UsuarioTienda
from apps.users.serializers.rol_tienda import AsignarRolTiendaSerializer
from apps.users.permissions import IsSuperUser


class UsuarioTiendaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioTienda.objects.all()
    serializer_class = AsignarRolTiendaSerializer
    permission_classes = [IsSuperUser]
