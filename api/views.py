from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from api.models import Company
from api.permissions import CompanyPermission, NewsPermission
from api.serializers import CompanySerializer, NewsSerializer, \
    CompanyDetailSerializer, ProfileSerializer
from user.models import Profile


class CompanyViewSet(ModelViewSet):
    """."""
    permission_classes = (CompanyPermission,)
    serializer_class = CompanySerializer
    action_serializers = {
        'retrieve': CompanyDetailSerializer,
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

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class NewsViewSet(ModelViewSet):
    """."""
    permission_classes = (IsAuthenticatedOrReadOnly, NewsPermission,)
    serializer_class = NewsSerializer

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        company = get_object_or_404(
            Company.objects.prefetch_related('news').all(),
            id=company_id,
        )
        print(company.news.all())
        return company.news.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProfileViewSet(ModelViewSet):
    """."""
    permission_classes = (IsAdminUser,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
