from rest_framework import serializers
from apps.ventas.models.venta import Venta, VentaProducto
from apps.ventas.models.cliente import Cliente


class VentaProductoReadSerializer(serializers.ModelSerializer):
    producto = serializers.CharField(source="lote_producto.producto.nombre")

    class Meta:
        model = VentaProducto
        fields = [
            "producto",
            "cantidad",
            "precio_venta"
        ]


class ClienteReadSerializer(serializers.ModelSerializer):
    saldo_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Cliente
        fields = [
            "id",
            "nombre",
            "telefono",
            "email",
            "saldo_total"
        ]


class VentaReadSerializer(serializers.ModelSerializer):
    detalle = VentaProductoReadSerializer(many=True)
    cliente = ClienteReadSerializer(read_only=True)

    class Meta:
        model = Venta
        fields = [
            "id",
            "tienda",
            "usuario_tienda",
            "cliente",
            "fecha",
            "metodo_pago",
            "es_credito",
            "total",
            "detalle"
        ]
