from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.users.models import Usuario
from apps.users.permissions import IsOwner
from apps.users.serializers.user_list import UsuarioListSerializer


class UsuarioListViewSet(ReadOnlyModelViewSet):
    serializer_class = UsuarioListSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Usuario.objects.filter(
            tiendas__isnull=True
        ).only(
            'id', 'first_name', 'last_name', 'is_active'
        )
