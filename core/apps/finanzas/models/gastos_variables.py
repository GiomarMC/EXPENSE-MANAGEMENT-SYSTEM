from django.db import models


class GastoVariable(models.Model):
    tienda = models.ForeignKey(
        'tiendas.Tienda',
        on_delete=models.CASCADE,
        related_name='gastos_variables'
    )

    descripcion = models.CharField(max_length=225)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
