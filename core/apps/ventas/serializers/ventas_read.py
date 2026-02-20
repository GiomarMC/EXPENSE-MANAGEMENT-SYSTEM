from rest_framework import serializers
from apps.ventas.models.venta import Venta, VentaProducto


class VentaProductoReadSerializer(serializers.ModelSerializer):
    producto = serializers.CharField(source="lote_producto.producto.nombre")

    class Meta:
        model = VentaProducto
        fields = [
            "producto",
            "cantidad",
            "precio_venta"
        ]


class VentaReadSerializer(serializers.ModelSerializer):
    detalle = VentaProductoReadSerializer(many=True)

    class Meta:
        model = Venta
        fields = [
            "id",
            "tienda",
            "usuario_tienda",
            "fecha",
            "metodo_pago",
            "total",
            "detalle"
        ]
