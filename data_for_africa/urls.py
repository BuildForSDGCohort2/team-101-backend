from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, static
from django.urls import path, include

import rest_framework.permissions as permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path, include

from .views import ping

schema_view = get_schema_view(
    openapi.Info(
        title = 'AfriData API',
        default_version = 'v1',
        description = 'Afridata application: A web application for uploading and downloading public datasets.',
        terms_of_service = 'https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ping, name='ping'),
    path('api/', include('accounts.urls')),
    path('api/services/', include('services.urls')),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+ static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
