from rest_framework import serializers
from apps.users.models import UsuarioTienda


class AsignarRolTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioTienda
        fields = ['usuario', 'tienda', 'rol', 'salario']
