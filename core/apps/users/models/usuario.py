from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    activo = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class UsuarioTienda(models.Model):
    usuario = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='tiendas'
    )

    tienda = models.ForeignKey(
        'tiendas.Tienda',
        on_delete=models.CASCADE,
        related_name='usuarios'
    )

    rol = models.ForeignKey(
        'users.Rol',
        on_delete=models.PROTECT
    )

    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.usuario} - {self.tienda} - {self.rol}"