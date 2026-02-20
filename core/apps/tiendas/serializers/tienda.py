from rest_framework import serializers
from apps.tiendas.models import Tienda
from apps.users.models import UsuarioTienda, Rol
from apps.users.constants import Roles
from django.db import transaction


class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = ['id', 'nombre_sede', 'direccion', "created_at"]

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]
        usuario = request.user

        tienda = Tienda.objects.create(
            id_duenio=usuario,
            **validated_data
        )

        rol_dueno = Rol.objects.get(nombre=Roles.DUENO)

        UsuarioTienda.objects.create(
            usuario=usuario,
            tienda=tienda,
            rol=rol_dueno,
            salario=0
        )

        return tienda
