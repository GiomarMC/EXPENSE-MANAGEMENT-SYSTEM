from apps.users.models import Usuario
from rest_framework import serializers


class UsuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'first_name', 'last_name', 'is_active')
