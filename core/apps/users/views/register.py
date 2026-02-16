from rest_framework.response import Response
from rest_framework import status, generics
from apps.users.permissions import IsSuperUser
from apps.users.serializers.register import CrearUsuarioSerializer


class CrearUsuarioView(generics.CreateAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = CrearUsuarioSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": f"Usuario '{user.username}' creado correctamente"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
