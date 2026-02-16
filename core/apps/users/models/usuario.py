from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q, CheckConstraint


class Usuario(AbstractUser):

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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

    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(salario__gte=0),
                name='salario_non_negative'
            )
        ]

    def __str__(self):
        return f"{self.usuario} - {self.tienda} - {self.rol}"
