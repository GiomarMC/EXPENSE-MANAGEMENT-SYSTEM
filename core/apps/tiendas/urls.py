from rest_framework.routers import DefaultRouter
from apps.tiendas.views.tienda import TiendaViewSet

router = DefaultRouter()
router.register(r'tiendas', TiendaViewSet, basename='tiendas')

urlpatterns = router.urls
