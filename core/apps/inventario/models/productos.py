from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
