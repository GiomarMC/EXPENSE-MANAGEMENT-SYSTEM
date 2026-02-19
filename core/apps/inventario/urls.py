from rest_framework.routers import DefaultRouter
from apps.inventario.views.producto import ProductoViewSet
from apps.inventario.views.lote import LoteViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='productos')
router.register(r'lotes', LoteViewSet, basename='lotes')

urlpatterns = router.urls
