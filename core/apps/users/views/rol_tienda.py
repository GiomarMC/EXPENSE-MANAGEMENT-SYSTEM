from rest_framework import viewsets
from apps.users.models import UsuarioTienda
from apps.users.serializers.rol_tienda import AsignarRolTiendaSerializer
from apps.users.permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class UsuarioTiendaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioTienda.objects.all()
    serializer_class = AsignarRolTiendaSerializer
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tienda', 'rol', 'usuario']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.usuario.is_active = False
        instance.usuario.save()
        return Response({"message": "Usuario desactivado"})
