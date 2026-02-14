from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializers import CustomTokenSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
