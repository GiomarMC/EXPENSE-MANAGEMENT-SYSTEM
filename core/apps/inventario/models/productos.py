from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre