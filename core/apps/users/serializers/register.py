from rest_framework import serializers
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = Usuario
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        )
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user
