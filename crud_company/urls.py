from django.contrib import admin
from django.urls import path, include

from user.views import CreateUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/registration/', CreateUserView.as_view({'post': 'create'}),
         name='registration'),
    path('api/auth/', include('rest_framework.urls')),

    path('api/', include('api.urls')),

]
