from rest_framework import mixins, viewsets, status
from apps.inventario.models.lotes import Lote
from apps.inventario.serializers.lote import (
    LoteCreateSerializer,
    LoteDetailSerializer
)
from apps.users.permissions import IsAdminOrOwner, IsWorkerOrAdminOrOwner
from rest_framework.response import Response


class LoteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Lote.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return LoteCreateSerializer
        return LoteDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAdminOrOwner()]
        return [IsWorkerOrAdminOrOwner()]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Lote.objects.all()

        if not hasattr(user, 'tiendas'):
            return Lote.objects.none()

        return Lote.objects.filter(
            tienda=user.tiendas.tienda
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lote = serializer.save()
        output_serializer = LoteDetailSerializer(lote)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
