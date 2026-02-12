from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nombre
