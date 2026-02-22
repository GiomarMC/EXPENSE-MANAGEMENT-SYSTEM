from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Lote(models.Model):
    tienda = models.ForeignKey(
        'tiendas.Tienda',
        on_delete=models.CASCADE,
        related_name='lotes'
    )

    fecha_llegada = models.DateField()
    costo_operacion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    costo_transporte = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Lote {self.id} - {self.tienda}"

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=['is_active'])
        self.productos.update(is_active=False)


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

    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    precio_venta_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('lote', 'producto')

    def __str__(self):
        return f"{self.producto} - {self.lote}"
