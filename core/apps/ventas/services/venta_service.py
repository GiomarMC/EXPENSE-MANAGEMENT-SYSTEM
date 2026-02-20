from django.db import transaction
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from apps.ventas.models.venta import Venta, VentaProducto
from apps.inventario.models.lotes import LoteProducto


class VentaService:

    @staticmethod
    @transaction.atomic
    def crear_venta(*, tienda, usuario_tienda, metodo_pago,
                    es_credito, cliente, productos):

        if es_credito and not cliente:
            raise ValidationError("Una venta a credito requiere cliente")

        venta = Venta.objects.create(
            tienda=tienda,
            usuario_tienda=usuario_tienda,
            metodo_pago=metodo_pago,
            es_credito=es_credito,
            cliente=cliente,
            total=0
        )

        total_venta = 0

        for item in productos:
            producto = item["producto"]
            cantidad_solicitada = item["cantidad"]
            precio_venta = item["precio_venta"]

            lotes = (
                LoteProducto.objects
                .select_for_update()
                .filter(
                    producto=producto,
                    lote__tienda=tienda,
                    cantidad_actual__gt=0
                )
                .order_by('lote__fecha_llegada')
            )

            total_disponible = lotes.aggregate(
                total=Sum('cantidad_actual')
            )["total"] or 0

            if total_disponible < cantidad_solicitada:
                raise ValidationError(
                    f"Stock insuficiente para el producto {producto.nombre}. "
                    f"Disponible: {total_disponible}"
                )

            cantidad_restante = cantidad_solicitada

            for lote in lotes:
                if cantidad_restante <= 0:
                    break

                descontar = min(lote.cantidad_actual, cantidad_restante)

                lote.cantidad_actual -= descontar
                lote.save(update_fields=['cantidad_actual'])

                VentaProducto.objects.create(
                    venta=venta,
                    lote_producto=lote,
                    cantidad=descontar,
                    precio_venta=precio_venta
                )

                total_venta += descontar * precio_venta
                cantidad_restante -= descontar

        venta.total = total_venta
        venta.save(update_fields=['total'])

        return venta
