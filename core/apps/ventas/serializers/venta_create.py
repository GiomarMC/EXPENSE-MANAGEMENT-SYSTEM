from rest_framework import serializers
from apps.inventario.models.productos import Producto
from apps.ventas.services.venta_service import VentaService
from apps.tiendas.models.tienda import Tienda
from apps.ventas.models.cliente import Cliente
from apps.users.models.usuario import UsuarioTienda


class VentaProductoInputSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False
    )


class VentaCreateSerializer(serializers.Serializer):
    tienda_id = serializers.IntegerField()
    metodo_pago = serializers.CharField()
    es_credito = serializers.BooleanField()
    cliente_id = serializers.IntegerField(required=False, allow_null=True)
    productos = VentaProductoInputSerializer(many=True)

    def validate(self, data):
        productos_input = data.get("productos", [])

        productos_procesados = []

        for item in productos_input:
            try:
                producto = Producto.objects.get(id=item["producto_id"])
            except Producto.DoesNotExist:
                raise serializers.ValidationError(
                    f"Producto con id {item['producto_id']} no existe"
                )

            precio_enviado = item.get("precio_venta")

            if precio_enviado is None:
                precio_final = producto.precio_venta_base
            else:
                if precio_enviado < producto.precio_venta_base:
                    raise serializers.ValidationError(
                        f"El precio de venta para {producto.nombre} "
                        f"no puede ser menor al precio base "
                        f"({producto.precio_venta_base})"
                    )
                precio_final = precio_enviado

            productos_procesados.append({
                "producto": producto,
                "cantidad": item["cantidad"],
                "precio_venta": precio_final
            })

        data["productos"] = productos_procesados

        return data

    def create(self, validate_data):
        request = self.context["request"]
        usuario = request.user

        tienda = Tienda.objects.get(
            id=validate_data["tienda_id"]
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

        cliente = None

        if validate_data.get("cliente_id"):
            cliente = Cliente.objects.get(
                id=validate_data["cliente_id"]
            )

        return VentaService.crear_venta(
            tienda=tienda,
            usuario_tienda=usuario_tienda,
            metodo_pago=validate_data["metodo_pago"],
            es_credito=validate_data["es_credito"],
            cliente=cliente,
            productos=validate_data["productos"]
        )
