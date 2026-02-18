from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from apps.users.models import Asistencia
from apps.users.permissions import IsAdminOfStore
from apps.users.serializers.asistencia import (
    MarcarEntradaSerializer,
    MarcarSalidaSerializer,
    AsistenciaSerializer
)
from rest_framework.response import Response


class AsistenciaViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Asistencia.objects.all()
    permission_classes = [IsAdminOfStore]

    def get_serializer_class(self):
        if self.action == "marcar_entrada":
            return MarcarEntradaSerializer
        elif self.action == "marcar_salida":
            return MarcarSalidaSerializer
        return AsistenciaSerializer

    @action(detail=False, methods=["post"], url_path="entrada")
    def marcar_entrada(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Entrada registrada"}, status=201)

    @action(detail=False, methods=["post"], url_path="salida")
    def marcar_salida(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Salida registrada"}, status=200)
