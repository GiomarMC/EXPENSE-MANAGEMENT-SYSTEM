from rest_framework import viewsets
from apps.users.permissions import IsOwner
from apps.tiendas.models import Tienda
from apps.tiendas.serializers.tienda import TiendaSerializer


class TiendaViewSet(viewsets.ModelViewSet):
    serializer_class = TiendaSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Tienda.objects.filter(id_duenio=self.request.user)
