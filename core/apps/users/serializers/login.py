from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


Usuario = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username_or_email = attrs.get('username')
        password = attrs.get('password')

        user = None

        if '@' in username_or_email:
            try:
                user_obj = Usuario.objects.get(email=username_or_email)
                username = user_obj.username
            except Usuario.DoesNotExist:
                raise serializers.ValidationError("Usuario no encontrado")
        else:
            username = username_or_email

        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Credenciales invalidas")

        attrs['username'] = username
        data = super().validate(attrs)

        return data
