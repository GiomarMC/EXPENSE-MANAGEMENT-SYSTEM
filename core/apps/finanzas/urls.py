from rest_framework.routers import DefaultRouter
from apps.finanzas.views.deuda import DeudaViewSet

router = DefaultRouter()
router.register(r'deudas', DeudaViewSet, basename="deudas")

urlpatterns = router.urls
