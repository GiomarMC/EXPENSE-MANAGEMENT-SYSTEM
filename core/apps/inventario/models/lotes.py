from django.db import models


class Lote(models.Model):
    tienda = models.ForeignKey(
        'tiendas.Tienda',
        on_delete=models.CASCADE,
        related_name='lotes'
    )

    fecha_llegada = models.DateField()
    costo_operacion = models.DecimalField(max_digits=10, decimal_places=2)
    costo_transporte = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Lote {self.id} - {self.tienda}"

class LoteProducto(models.Model):
    lote = models.ForeignKey(
        'inventario.Lote',
        on_delete=models.CASCADE,
        related_name='productos'
    )

    producto = models.ForeignKey(
        'inventario.Producto',
        on_delete=models.PROTECT
    )

    cantidad_inicial = models.PositiveIntegerField()
    cantidad_actual = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto} - {self.lote}"
