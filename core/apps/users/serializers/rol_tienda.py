from rest_framework import serializers
from apps.users.models import UsuarioTienda
from apps.users.models import Usuario


class UsuarioTiendaDetailSerializer(serializers.ModelSerializer):
    usuario_id = serializers.IntegerField(source='usuario.id')
    usuario_nombre = serializers.SerializerMethodField()
    usuario_is_active = serializers.BooleanField(source='usuario.is_active')

    tienda_id = serializers.IntegerField(source='tienda.id')
    tienda_nombre = serializers.CharField(source='tienda.nombre_sede')

    rol_id = serializers.IntegerField(source='rol.id')
    rol_nombre = serializers.CharField(source='rol.nombre')

    class Meta:
        model = UsuarioTienda
        fields = [
            'id',
            'usuario_id',
            'usuario_nombre',
            'usuario_is_active',
            'tienda_id',
            'tienda_nombre',
            'rol_id',
            'rol_nombre',
            'salario'
        ]

    def get_usuario_nombre(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}"


class AsignarRolTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioTienda
        fields = ['usuario', 'tienda', 'rol', 'salario']

    def validate_usuario(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                "El usuario no esta activo"
            )
        return value


class UsuarioTiendaMeSerializer(serializers.ModelSerializer):
    tienda_id = serializers.IntegerField(source='tienda.id')
    tienda_nombre = serializers.CharField(source='tienda.nombre_sede')
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
        try:
            relacion = obj.tiendas
        except UsuarioTienda.DoesNotExist:
            return None
        return UsuarioTiendaMeSerializer(relacion).data
