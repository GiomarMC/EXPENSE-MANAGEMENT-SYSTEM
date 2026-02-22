from rest_framework.viewsets import ModelViewSet
from apps.finanzas.serializers.deuda import DeudaReadSerializer
from apps.finanzas.models.deudas import Deuda
from apps.users.permissions import IsAdminOrOwner


class DeudaViewSet(ModelViewSet):
    queryset = Deuda.objects.select_related("cliente", "venta")
    serializer_class = DeudaReadSerializer
    permission_classes = [IsAdminOrOwner]
