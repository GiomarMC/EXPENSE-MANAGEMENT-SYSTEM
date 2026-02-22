from django.db import transaction
from django.core.exceptions import ValidationError
from apps.inventario.models import Lote, LoteProducto, Producto


class LoteService:

    @staticmethod
    @transaction.atomic
    def crear_lote_completo(data, user):
        productos_data = data.pop('productos')

        productos_resueltos = []

        for item in productos_data:
            producto_id = item.get("producto_id")
            nombre = item.get("nombre")

            if producto_id:
                try:
                    producto = Producto.objects.get(
                        id=producto_id,
                        is_active=True
                    )
                except Producto.DoesNotExist:
                    raise ValidationError(
                        f"Producto {nombre} no existe o esta inactivo"
                    )
            else:
                producto, _ = Producto.objects.get_or_create(
                    nombre=nombre.strip(),
                    defaults={"is_active": True}
                )

            productos_resueltos.append(
                (producto, item)
            )

        lote = Lote.objects.create(**data)

        lote_productos = []

        for producto, item in productos_resueltos:
            lote_productos.append(
                LoteProducto(
                    lote=lote,
                    producto=producto,
                    cantidad_inicial=item["cantidad"],
                    cantidad_actual=item["cantidad"],
                    precio_compra=item["precio_compra"],
                    precio_venta_base=item["precio_venta_base"]
                )
            )

        LoteProducto.objects.bulk_create(lote_productos)

        return lote
