from rest_framework import serializers
from apps.users.models import Asistencia
from django.utils import timezone


class MarcarEntradaSerializer(serializers.ModelSerializer):
    usuario_tienda = serializers.IntegerField()

    class Meta:
        model = Asistencia
        fields = ['usuario_tienda']
        read_only_fields = ['fecha', 'hora_entrada']

    def validate(self, data):
        usuario_tienda = data["usuario_tienda"]
        hoy = timezone.localdate()

        if Asistencia.objects.filter(
            usuario_tienda_id=usuario_tienda,
            fecha=hoy
        ).exists():
            raise serializers.ValidationError(
                "Ya existe una asistencia registrada hoy"
            )

        return data

    def create(self, validated_data):
        return Asistencia.objects.create(
            usuario_tienda_id=validated_data["usuario_tienda"],
            fecha=timezone.localdate(),
            hora_entrada=timezone.localtime().time()
        )


class MarcarSalidaSerializer(serializers.ModelSerializer):
    usuario_tienda = serializers.IntegerField()

    class Meta:
        model = Asistencia
        fields = ['usuario_tienda']
        read_only_fields = ['fecha', 'hora_salida']

    def validate(self, data):
        usuario_tienda = data["usuario_tienda"]
        hoy = timezone.localdate()

        try:
            asistencia = Asistencia.objects.get(
                usuario_tienda_id=usuario_tienda,
                fecha=hoy
            )
        except Asistencia.DoesNotExist:
            raise serializers.ValidationError(
                "No existe una asistencia registrada hoy"
            )

        if asistencia.hora_salida:
            raise serializers.ValidationError(
                "La salida ya fue registrada"
            )

        data["asistencia"] = asistencia
        return data

    def save(self):
        asistencia = self.validated_data["asistencia"]
        asistencia.hora_salida = timezone.localtime().time()
        asistencia.save()
        return asistencia


class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = "__all__"
