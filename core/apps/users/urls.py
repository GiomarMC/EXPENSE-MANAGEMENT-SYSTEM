from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views.register import RegistroView
from .views.login import CustomLoginView

urlpatterns = [
    path('register/', RegistroView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
