from django.db import models


class Asistencia(models.Model):
    usuario_tienda = models.ForeignKey(
        'users.UsuarioTienda',
        on_delete=models.CASCADE,
        related_name='asistencias'
    )

    fecha = models.DateField()
    hora_entrada = models.TimeField(blank=True, null=True)
    hora_salida = models.TimeField(blank=True, null=True)
    default = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario_tienda', 'fecha')

    def __str__(self):
        return f"{self.usuario_tienda} - {self.fecha}"
