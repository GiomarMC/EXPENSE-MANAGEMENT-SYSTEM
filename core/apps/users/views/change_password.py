from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from apps.users.serializers.change_password import ChangePasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Contraseña actualizada correctamente'}
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
