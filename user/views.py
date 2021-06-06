from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import UserSerializer


class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    """Регистрация пользователя."""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
