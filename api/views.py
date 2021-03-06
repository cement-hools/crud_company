from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from api.models import Company
from api.permissions import CompanyPermission, NewsPermission
from api.serializers import CompanySerializer, NewsSerializer, \
    CompanyDetailSerializer, ProfileSerializer
from user.models import Profile


class CompanyViewSet(ModelViewSet):
    """Вьюсет компаний."""
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
        queryset = Company.objects.all()
        return queryset


class NewsViewSet(ModelViewSet):
    """Вьюсет новостей."""
    permission_classes = (IsAuthenticatedOrReadOnly, NewsPermission,)
    serializer_class = NewsSerializer

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        company = get_object_or_404(
            Company.objects.prefetch_related('news').all(),
            id=company_id,
        )
        return company.news.all()

    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        company = get_object_or_404(
            Company.objects.prefetch_related('news').all(),
            id=company_id,
        )
        serializer.save(author=self.request.user, company=company)


class ProfileViewSet(ModelViewSet):
    """Вьюсет профилей."""
    permission_classes = (IsAdminUser,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
