from rest_framework.permissions import BasePermission
from .models import UsuarioTienda


class IsAdminOROwner(BasePermission):
    
    def has_permission(self, request, view):
        tienda_id = view.kwargs.get("tienda_id")

        if not tienda_id:
            return False
        
        try:
            usuario_tienda = UsuarioTienda.objects.get(
                usuario=request.user,
                tienda_id=tienda_id,
                activo=True
            )

            return usuario_tienda.rol.nombre in ["ADMINISTRADOR", "DUENO"]
        except UsuarioTienda.DoesNotExist:
            return False
