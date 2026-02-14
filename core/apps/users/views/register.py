from rest_framework import generics
from django.contrib.auth import get_user_model
from apps.users.serializers import RegistroSerializer

Usuario = get_user_model()


class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = []
