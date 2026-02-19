from django.db import models


class CajaDiaria(models.Model):
    ESTADOS = [
        ('CORRECTO', 'Correcto'),
        ('PENDIENTE', 'Pendiente'),
    ]

    tienda = models.ForeignKey(
        'tiendas.Tienda',
        on_delete=models.CASCADE,
        related_name='cajas'
    )

    usuario_tienda = models.ForeignKey(
        'users.UsuarioTienda',
        on_delete=models.PROTECT
    )

    fecha_hora = models.DateTimeField(auto_now_add=True)

    monto_esperado = models.DecimalField(max_digits=10, decimal_places=2)
    monto_real = models.DecimalField(max_digits=10, decimal_places=2)

    diferencia = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS)

    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Caja {self.id} - {self.tienda} - {self.fecha_hora}"
