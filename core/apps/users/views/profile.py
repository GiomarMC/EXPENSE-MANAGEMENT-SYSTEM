from rest_framework import generics
from apps.users.permissions import IsWorkerOrAdminOrOwner
from apps.users.serializers.register import CompletarPerfilSerializer
from rest_framework.generics import RetrieveAPIView
from apps.users.serializers.rol_tienda import MeSerializer


class CompletarPerfilView(generics.UpdateAPIView):
    serializer_class = CompletarPerfilSerializer
    permission_classes = [IsWorkerOrAdminOrOwner]

    def get_object(self):
        return self.request.user


class MeView(RetrieveAPIView):
    permission_classes = [IsWorkerOrAdminOrOwner]
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user
