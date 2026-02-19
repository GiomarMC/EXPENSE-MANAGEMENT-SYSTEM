from apps.users.permissions import IsWorkerOrAdminOrOwner
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from apps.users.serializers.change_password import ChangePasswordSerializer


class ChangePasswordView(GenericAPIView):
    permission_classes = [IsWorkerOrAdminOrOwner]
    serializer_class = ChangePasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Contraseña actualizada correctamente"},
            status=status.HTTP_200_OK
        )
