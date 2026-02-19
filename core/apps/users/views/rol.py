from rest_framework import viewsets
from apps.users.permissions import IsOwnerOnly
from apps.users.models import Rol
from apps.users.serializers.rol import RolSerializer


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsOwnerOnly]
