from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CompanyViewSet, NewsViewSet, ProfileViewSet

company_router = DefaultRouter()
company_router.register('companies', CompanyViewSet, basename='companies')
company_router.register(
    r'companies/(?P<company_id>\d+)/news',
    NewsViewSet,
    basename='news'
)
profile_router = DefaultRouter()
profile_router.register('profiles', ProfileViewSet, basename='profiles')

urlpatterns = [

    path('v1/', include(company_router.urls)),
    path('v1/', include(profile_router.urls)),

]
