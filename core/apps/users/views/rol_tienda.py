from rest_framework import viewsets, status
from apps.users.models import UsuarioTienda
from apps.users.serializers.rol_tienda import (
    AsignarRolTiendaSerializer,
    UsuarioTiendaDetailSerializer
)
from apps.users.permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.users.models import Usuario


class UsuarioTiendaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tienda', 'rol', 'usuario']

    def get_queryset(self):
        return UsuarioTienda.objects.select_related(
            'usuario',
            'tienda',
            'rol'
        ).all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UsuarioTiendaDetailSerializer
        return AsignarRolTiendaSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["patch"], serializer_class=None)
    def toggle_usuario(self, request, pk=None):
        usuario = get_object_or_404(Usuario, id=pk)
        usuario.is_active = not usuario.is_active
        usuario.save(update_fields=['is_active'])

        return Response(
            {
                "id": usuario.id,
                "is_active": usuario.is_active,
            },
            status=status.HTTP_200_OK
        )
