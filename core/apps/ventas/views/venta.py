from rest_framework.viewsets import ModelViewSet
from apps.users.permissions import IsAdminOrOwner
from apps.ventas.models.venta import Venta
from apps.ventas.serializers.venta_create import VentaCreateSerializer
from apps.ventas.serializers.ventas_read import VentaReadSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.ventas.filters import VentaFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError


class VentaViewSet(ModelViewSet):
    queryset = Venta.objects.select_related(
        "tienda",
        "usuario_tienda",
        "cliente"
    )

    permission_classes = [IsAdminOrOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VentaFilter

    search_fields = [
        "cliente__nombre",
        "cliente__telefono",
        "cliente__email"
    ]

    ordering_fields = ["fecha", "total"]
    ordering = ["-fecha"]

    def get_queryset(self):
        user = self.request.user

        return Venta.objects.filter(
            tienda__id_duenio=user,
            is_active=True
        ).select_related(
            "tienda",
            "usuario_tienda",
            "cliente"
        )

    def get_serializer_class(self):
        if self.action == "create":
            return VentaCreateSerializer
        return VentaReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        venta = serializer.save()

        read_serializer = VentaReadSerializer(venta)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        if not instance.is_active:
            raise ValidationError("La venta ya ha sidoo desactivada")

        for item in instance.detalle.all():
            lote_produdcto = item.lote_producto
            lote_produdcto.cantidad_actual += item.cantidad
            lote_produdcto.save(update_fields=['cantidad_actual'])

        instance.is_active = False
        instance.save(update_fields=['is_active'])
