from rest_framework import serializers
from apps.finanzas.models.deudas import PagoDeuda, Deuda


class PagoDeudaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoDeuda
        fields = ["fecha", "monto"]


class DeudaReadSerializer(serializers.ModelSerializer):
    pagos = PagoDeudaSerializer(many=True)
    venta_id = serializers.IntegerField(
        source="venta.id",
        read_only=True
    )

    class Meta:
        model = Deuda
        fields = [
            "id",
            "venta_id",
            "monto_total",
            "saldo",
            "estado",
            "pagos"
        ]
