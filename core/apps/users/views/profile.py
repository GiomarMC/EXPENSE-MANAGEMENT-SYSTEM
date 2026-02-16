from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers.register import CompletarPerfilSerializer


class CompletarPerfilView(generics.UpdateAPIView):
    serializer_class = CompletarPerfilSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
