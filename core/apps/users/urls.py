from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from apps.users.views.profile import CompletarPerfilView, MeView
from apps.users.views.change_password import ChangePasswordView
from apps.users.views.login import CustomTokenObtainPairView
from apps.users.views.register import CrearUsuarioView
from apps.users.views.rol_tienda import UsuarioTiendaViewSet
from apps.users.views.asistencia import AsistenciaViewSet
from apps.users.views.rol import RolViewSet
from apps.users.views.user_list import UsuarioListViewSet

router = DefaultRouter()
router.register(r'usuario-tienda', UsuarioTiendaViewSet,
                basename='usuario-tienda')
router.register(r'asistencia', AsistenciaViewSet, basename='asistencia')
router.register(r'roles', RolViewSet, basename='roles')
router.register(r'usuarios', UsuarioListViewSet, basename='usuarios')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/complete/', CompletarPerfilView.as_view(),
         name='profile_complete'),
    path('profile/change_password/', ChangePasswordView.as_view(),
         name='change-password'),
    path('register/', CrearUsuarioView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),
]

urlpatterns += router.urls
