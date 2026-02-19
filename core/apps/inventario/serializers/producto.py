from rest_framework import serializers
from apps.inventario.models.productos import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"
        read_only_fields = ['id']
