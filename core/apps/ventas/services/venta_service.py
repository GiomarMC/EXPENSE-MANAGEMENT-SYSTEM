from django.db import transaction
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from apps.ventas.models.venta import Venta, VentaProducto
from apps.inventario.models.lotes import LoteProducto
from apps.finanzas.models.deudas import Deuda


class VentaService:

    @staticmethod
    @transaction.atomic
    def crear_venta(*, tienda, usuario_tienda, metodo_pago,
                    es_credito, cliente, productos):

        VentaService._validar_credito(es_credito, cliente)

        venta = VentaService._crear_venta_base(
            tienda, usuario_tienda, metodo_pago, es_credito, cliente
        )

        total = VentaService._procesar_productos(
            venta, tienda, productos
        )

        venta.total = total
        venta.save(update_fields=["total"])

        if es_credito:
            VentaService._crear_deuda(cliente, venta, total)

        return venta

    @staticmethod
    def _crear_venta_base(tienda, usuario_tienda,
                          metodo_pago, es_credito, cliente):
        return Venta.objects.create(
            tienda=tienda,
            usuario_tienda=usuario_tienda,
            metodo_pago=metodo_pago,
            es_credito=es_credito,
            cliente=cliente,
            total=0
        )

    @staticmethod
    def _procesar_productos(venta, tienda, productos):
        total_venta = 0

        for item in productos:
            total_venta += VentaService._procesar_producto_individual(
                venta, tienda, item
            )

        return total_venta

    @staticmethod
    def _procesar_producto_individual(venta, tienda, item):
        producto = item["producto"]
        cantidad_solicitada = item["cantidad"]
        precio_enviado = item.get("precio_venta")

        lotes = (
            LoteProducto.objects
            .select_for_update()
            .filter(
                producto=producto,
                lote__tienda=tienda,
                cantidad_actual__gt=0,
                is_active=True
            )
            .order_by("lote__fecha_llegada")
        )

        total_disponible = lotes.aggregate(
            total=Sum("cantidad_actual")
        )["total"] or 0

        if total_disponible < cantidad_solicitada:
            raise ValidationError(
                f"Stock insuficiente para {producto.nombre}. "
                f"Disponible: {total_disponible}"
            )

        cantidad_restante = cantidad_solicitada
        total_producto = 0

        for lote in lotes:
            if cantidad_restante <= 0:
                break

            precio_final = VentaService._resolver_precio(
                lote, precio_enviado, producto
            )

            descontar = min(lote.cantidad_actual, cantidad_restante)

            lote.cantidad_actual -= descontar
            lote.save(update_fields=["cantidad_actual"])

            VentaProducto.objects.create(
                venta=venta,
                lote_producto=lote,
                cantidad=descontar,
                precio_venta=precio_final
            )

            total_producto += descontar * precio_final
            cantidad_restante -= descontar

        return total_producto

    @staticmethod
    def _resolver_precio(lote, precio_enviado, producto):
        precio_base = lote.precio_venta_base

        if precio_enviado is None:
            return precio_base

        if precio_enviado < precio_base:
            raise ValidationError(
                f"El precio no puede ser menor al precio base "
                f"({precio_base}) para {producto.nombre}"
            )

        return precio_enviado

    @staticmethod
    def _crear_deuda(cliente, venta, total):
        Deuda.objects.create(
            cliente=cliente,
            venta=venta,
            monto_total=total,
            saldo=total,
            estado="ACTIVA"
        )

    @staticmethod
    def _validar_credito(es_credito, cliente):
        if es_credito and not cliente:
            raise ValidationError(
                "Una venta a credito requiere un cliente valido"
            )

        if not es_credito and cliente:
            raise ValidationError(
                "Una venta al contado no debe tener cliente asociado"
            )
