from django.db import models


class Venta(models.Model):
    tienda = models.ForeignKey(
        'tiendas.Tienda',
        on_delete=models.CASCADE,
        related_name='ventas'
    )

    usuario_tienda = models.ForeignKey(
        'users.UsuarioTienda',
        on_delete=models.PROTECT
    )

    cliente = models.ForeignKey(
        'ventas.Cliente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=30)

    es_credito = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id} - {self.tienda} - {self.fecha}"


class VentaProducto(models.Model):
    venta = models.ForeignKey(
        'ventas.Venta',
        on_delete=models.CASCADE,
        related_name='detalle'
    )

    producto = models.ForeignKey(
        'inventario.Producto',
        on_delete=models.PROTECT
    )

    lote = models.ForeignKey(
        'inventario.Lote',
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto} - {self.venta} - {self.lote}"