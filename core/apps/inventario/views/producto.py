from rest_framework import viewsets
from apps.inventario.serializers.producto import ProductoSerializer
from apps.inventario.models.productos import Producto
from apps.users.permissions import IsAdminOrOwner, IsWorkerOrAdminOrOwner


class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsWorkerOrAdminOrOwner()]
        return [IsAdminOrOwner()]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])
