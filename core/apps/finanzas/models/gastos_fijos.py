from django.db import models


class GastoFijo(models.Model):
    tienda = models.ForeignKey(
        'tiendas.Tienda',
        on_delete=models.CASCADE,
        related_name='gastos_fijos'
    )

    descripcion = models.CharField(max_length=255, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    dia_pago = models.PositiveIntegerField()
