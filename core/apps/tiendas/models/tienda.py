from django.db import models


class Tienda(models.Model):
    nombre_sede = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)

    id_duenio = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='tiendas_duenio'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_sede
