from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
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

    def __str__(self):
        return self.nombre
