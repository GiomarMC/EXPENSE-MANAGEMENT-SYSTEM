from rest_framework import serializers
from apps.ventas.services.venta_service import VentaService
from apps.tiendas.models.tienda import Tienda
from apps.ventas.models.cliente import Cliente
from apps.users.models.usuario import UsuarioTienda
from apps.inventario.models.productos import Producto


class VentaProductoInputSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)
    precio_venta = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False
    )


class ClienteInputSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=False)
    telefono = serializers.CharField(required=False)
    email = serializers.EmailField(required=False, allow_null=True)


class VentaCreateSerializer(serializers.Serializer):
    tienda_id = serializers.IntegerField()
    metodo_pago = serializers.CharField()
    es_credito = serializers.BooleanField()
    cliente_id = serializers.IntegerField(required=False, allow_null=True)
    cliente = ClienteInputSerializer(required=False)
    productos = VentaProductoInputSerializer(many=True)

    def validate(self, data):
        es_credito = data.get("es_credito")
        cliente_id = data.get("cliente_id")
        cliente_data = data.get("cliente")

        if es_credito:
            if not cliente_id and not cliente_data:
                raise serializers.ValidationError(
                    "Una venta a credito requiere cliente"
                )

            if cliente_id and cliente_data:
                raise serializers.ValidationError(
                    (
                        "No puede proporcionar un cliente existente y un "
                        "cliente nuevo al mismo tiempo"
                    )
                )

        productos = data.get("productos", [])

        if not productos:
            raise serializers.ValidationError(
                "Debe agregar al menos un producto"
            )

        productos_ids = [item["producto_id"] for item in productos]

        if len(productos_ids) != len(set(productos_ids)):
            raise serializers.ValidationError(
                "No puede repetir el mismo producto en la venta"
            )

        return data

    def create(self, validated_data):
        request = self.context["request"]
        usuario = request.user
        productos_input = validated_data["productos"]
        productos_resueltos = []

        for item in productos_input:
            try:
                producto = Producto.objects.get(
                    id=item["producto_id"],
                    is_active=True
                )
            except Producto.DoesNotExist:
                raise serializers.ValidationError(
                    "El producto no existe"
                )

            productos_resueltos.append({
                "producto": producto,
                "cantidad": item["cantidad"],
                "precio_venta": item.get("precio_venta")
            })

        tienda = Tienda.objects.get(
            id=validated_data["tienda_id"]
        )

        try:
            usuario_tienda = UsuarioTienda.objects.get(
                usuario=usuario,
                tienda=tienda
            )
        except UsuarioTienda.DoesNotExist:
            raise serializers.ValidationError(
                "El usuario no tiene acceso a esta tienda"
            )

        cliente_data = validated_data.get("cliente")
        cliente = None

        if validated_data["es_credito"]:
            cliente_id = validated_data.get("cliente_id")
            cliente_data = validated_data.get("cliente")

            if cliente_id:
                try:
                    cliente = Cliente.objects.get(id=cliente_id)
                except Cliente.DoesNotExist:
                    raise serializers.ValidationError(
                        "El cliente proporcionado no existe"
                    )
            else:
                cliente = Cliente.objects.create(
                    nombre=cliente_data["nombre"],
                    telefono=cliente_data["telefono"],
                    email=cliente_data.get("email")
                )

        return VentaService.crear_venta(
            tienda=tienda,
            usuario_tienda=usuario_tienda,
            metodo_pago=validated_data["metodo_pago"],
            es_credito=validated_data["es_credito"],
            cliente=cliente,
            productos=productos_resueltos
        )
