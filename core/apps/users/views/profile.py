from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers.register import CompletarPerfilSerializer
from rest_framework.generics import RetrieveAPIView
from apps.users.serializers.rol_tienda import MeSerializer


class CompletarPerfilView(generics.UpdateAPIView):
    serializer_class = CompletarPerfilSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class MeView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user
