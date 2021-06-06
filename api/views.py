from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.models import Company
from api.permissions import CustomPermission
from api.serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    """."""
    permission_classes = (IsAuthenticatedOrReadOnly, CustomPermission,)
    serializer_class = CompanySerializer
    action_serializers = {
        'retrieve': CompanySerializer,
        'list': CompanySerializer,
        'create': CompanySerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action,
                                               self.serializer_class)

        return super(CompanyViewSet, self).get_serializer_class()

    def get_queryset(self):
        # queryset = Wallet.objects.filter(owner=self.request.user)
        queryset = Company.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
