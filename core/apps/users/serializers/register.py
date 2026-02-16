import random
import string
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from apps.users.models import UsuarioTienda
from apps.users.models import Rol
from apps.tiendas.models import Tienda

Usuario = get_user_model()


def generar_password(longitud=10):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))


class CrearUsuarioSerializer(serializers.ModelSerializer):
    tienda = serializers.PrimaryKeyRelatedField(
        queryset=Tienda.objects.all(),
        required=False,
    )
    rol = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(),
        required=False,
    )
    salario = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    class Meta:
        model = Usuario
        fields = ['email', 'tienda', 'rol', 'salario']

    def create(self, validated_data):
        tienda = validated_data.pop('tienda', None)
        rol = validated_data.pop('rol', None)
        salario = validated_data.pop('salario', None)

        email = validated_data['email']
        username = email.split('@')[0]
        password = generar_password()
        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=True
        )

        if tienda and rol:
            UsuarioTienda.objects.create(
                usuario=user,
                tienda=tienda,
                rol=rol,
                salario=salario or 0
            )

        send_mail(
            'Bienvenido a Expense Management System',
            'Tus credenciales de acceso son:\n\n'
            f'Usuario: {username}\n'
            f'Contraseña: {password}\n',
            'noreply@sistema.com',
            [email],
        )

        return user


class CompletarPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name']
