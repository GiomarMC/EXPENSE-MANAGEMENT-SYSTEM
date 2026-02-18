from rest_framework import serializers
from apps.tiendas.models import Tienda


class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = ['id', 'nombre_sede', 'direccion', "created_at"]

    def create(self, validated_data):
        request = self.context["request"]
        return Tienda.objects.create(
            id_duenio=request.user,
            **validated_data
        )
