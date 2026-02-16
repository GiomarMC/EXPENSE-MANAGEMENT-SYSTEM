from rest_framework import serializers
from apps.users.models import UsuarioTienda
from apps.users.models import Usuario


class AsignarRolTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioTienda
        fields = ['usuario', 'tienda', 'rol', 'salario']


class UsuarioTiendaMeSerializer(serializers.ModelSerializer):
    tienda_id = serializers.IntegerField(source='tienda.id')
    tienda_nombre = serializers.CharField(source='tienda.nombre')
    rol = serializers.CharField(source='rol.nombre')

    class Meta:
        model = UsuarioTienda
        fields = ['tienda_id', 'tienda_nombre', 'rol', 'salario']


class MeSerializer(serializers.ModelSerializer):
    tiendas = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_superuser",
            "tiendas"
        ]

    def get_tiendas(self, obj):
        relaciones = obj.tiendas.select_related(
            "tienda",
            "rol"
        ).all()

        return UsuarioTiendaMeSerializer(relaciones, many=True).data
