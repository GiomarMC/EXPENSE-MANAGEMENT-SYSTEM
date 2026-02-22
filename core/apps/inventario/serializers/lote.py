from rest_framework import serializers
from apps.inventario.models.lotes import Lote, LoteProducto
from apps.inventario.services.lote_service import LoteService
from apps.tiendas.models import Tienda


class LoteProductoInputSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(required=False)

    cantidad = serializers.IntegerField(min_value=1)
    precio_compra = serializers.DecimalField(max_digits=10, decimal_places=2)
    precio_venta_base = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )

    def validate(self, data):
        if not data.get('producto_id') and not data.get('nombre'):
            raise serializers.ValidationError(
                "Debe proporcionar un producto"
            )

        return data


class LoteCreateAtomicSerializer(serializers.Serializer):
    tienda = serializers.PrimaryKeyRelatedField(
        queryset=Tienda.objects.all()
    )
    fecha_llegada = serializers.DateField()
    costo_operacion = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )
    costo_transporte = serializers.DecimalField(
        max_digits=10, decimal_places=2
    )

    productos = LoteProductoInputSerializer(many=True)

    def validate_productos(self, value):
        if not value:
            raise serializers.ValidationError(
                "Debe agregar al menos un producto al lote"
            )
        return value

    def validate(self, attrs):
        productos = attrs.get("productos", [])

        productos_ids = []
        productos_nombres = []

        for item in productos:
            if item.get("producto_id"):
                productos_ids.append(item["producto_id"])
            elif item.get("nombre"):
                productos_nombres.append(item["nombre"].strip().lower())

        if len(productos_ids) != len(set(productos_ids)):
            raise serializers.ValidationError(
                "No puede repetir el mismo producto en el lote"
            )

        if len(productos_nombres) != len(set(productos_nombres)):
            raise serializers.ValidationError(
                "No puede repetir productos con el mismo nombre"
            )

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return LoteService.crear_lote_completo(validated_data, user)


class LoteProductoDetailSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source='producto.nombre',
        read_only=True
    )

    class Meta:
        model = LoteProducto
        fields = [
            "id",
            "producto",
            "producto_nombre",
            "cantidad_inicial",
            "cantidad_actual",
            "precio_compra",
            "precio_venta_base",
            "is_active"
        ]


class LoteDetailSerializer(serializers.ModelSerializer):
    productos = LoteProductoDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Lote
        fields = [
            "id",
            "tienda",
            "fecha_llegada",
            "costo_operacion",
            "costo_transporte",
            "is_active",
            "productos"
        ]
