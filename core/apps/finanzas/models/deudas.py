from django.db import models


class Deuda(models.Model):
    ESTADOS = [
        ('ACTIVA', 'Activa'),
        ('PAGADA', 'Pagada'),
    ]

    cliente = models.ForeignKey(
        'ventas.Cliente',
        on_delete=models.CASCADE,
        related_name='deudas'
    )

    venta = models.ForeignKey(
        'ventas.Venta',
        on_delete=models.CASCADE,
        related_name='deuda'
    )

    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS)


class PagoDeuda(models.Model):
    deuda = models.ForeignKey(
        'finanzas.Deuda',
        on_delete=models.CASCADE,
        related_name='pagos'
    )

    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
