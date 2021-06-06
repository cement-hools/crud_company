from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from api.models import Company
from api.permissions import CustomPermission
from api.serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    """."""
    permission_classes = (CustomPermission,)
    serializer_class = CompanySerializer

    def get_queryset(self):
        # queryset = Wallet.objects.filter(owner=self.request.user)
        queryset = Company.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
