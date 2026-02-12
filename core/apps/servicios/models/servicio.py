from django.db import models


class Servicio(models.Model):
    tienda = models.ForeignKey(
        'tiendas.Tienda',
        on_delete=models.CASCADE,
        related_name='servicios'
    )

    usuario_tienda = models.ForeignKey(
        'users.UsuarioTienda',
        on_delete=models.PROTECT
    )

    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    costo = models.DecimalField(max_digits=10, decimal_places=2)
    es_credito = models.BooleanField(default=False)
