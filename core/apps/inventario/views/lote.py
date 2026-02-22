from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import mixins, viewsets, status
from apps.inventario.models.lotes import Lote
from apps.inventario.serializers.lote import (
    LoteCreateAtomicSerializer,
    LoteDetailSerializer
)
from rest_framework.response import Response
from apps.users.permissions import IsAdminOrOwner, IsWorkerOrAdminOrOwner


class LoteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Lote.objects.none()

        user = self.request.user

        return Lote.objects.filter(
            is_active=True,
            tienda__in=user.tiendas.values_list("tienda_id", flat=True)
        ).select_related(
            "tienda"
        ).prefetch_related(
            "productos__producto"
        )

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsWorkerOrAdminOrOwner()]
        return [IsAdminOrOwner()]

    def get_serializer_class(self):
        if self.action == "create":
            return LoteCreateAtomicSerializer
        return LoteDetailSerializer

    @extend_schema(
            request=LoteCreateAtomicSerializer,
            responses={201: LoteDetailSerializer},
            examples=[
                OpenApiExample(
                    "Crear lote con producto existente",
                    value={
                        "tienda": 1,
                        "fecha_llegada": "2024-01-01",
                        "costo_operacion": "100.00",
                        "costo_transporte": "50.00",
                        "productos": [
                            {
                                "producto_id": 1,
                                "cantidad": 10,
                                "precio_compra": "20.00",
                                "precio_venta_base": "30.00"
                            }
                        ]
                    }
                ),
                OpenApiExample(
                    "Crear lote con producto nuevo",
                    value={
                        "tienda": 1,
                        "fecha_llegada": "2024-01-01",
                        "costo_operacion": "100.00",
                        "costo_transporte": "50.00",
                        "productos": [
                            {
                                "nombre": "Producto Nuevo",
                                "cantidad": 5,
                                "precio_compra": "15.00",
                                "precio_venta_base": "25.00"
                            }
                        ]
                    }
                ),
            ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lote = serializer.save()

        output_serializer = LoteDetailSerializer(
            lote,
            context=self.get_serializer_context()
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.deactivate()
