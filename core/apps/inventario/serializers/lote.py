from django.db import transaction
from rest_framework import serializers
from apps.inventario.models.lotes import Lote, LoteProducto
from apps.inventario.models.productos import Producto


class LoteProductoCreateSerializer(serializers.Serializer):
    producto = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.filter(is_active=True)
    )
    cantidad = serializers.IntegerField(min_value=1)


class LoteCreateSerializer(serializers.ModelSerializer):
    productos = LoteProductoCreateSerializer(many=True)

    class Meta:
        model = Lote
        fields = [
            "id",
            "tienda",
            "fecha_llegada",
            "costo_operacion",
            "costo_transporte",
            "productos"
        ]
    read_only_fields = ['id']

    def validate_tienda(self, tienda):
        request = self.context['request']
        user = request.user

        if user.is_superuser:
            return tienda

        pertenece = user.tiendas.filter(
            tienda=tienda,
            rol__nombre='ADMINISTRADOR'
        ).exists()

        if not pertenece:
            raise serializers.ValidationError(
                "No tienes permisos para agregar un lote a esta tienda."
            )
        return tienda

    @transaction.atomic
    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        lote = Lote.objects.create(**validated_data)

        LoteProducto.objects.bulk_create([
            LoteProducto(
                lote=lote,
                producto=item['producto'],
                cantidad_inicial=item['cantidad'],
                cantidad_actual=item['cantidad']
            ) for item in productos_data
        ])

        return lote


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
            "cantidad_actual"
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
            "productos"
        ]
