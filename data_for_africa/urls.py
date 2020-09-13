# Core Django imports
from django.contrib import admin
from django.urls import path, include

# Imports from apps
from .views import ping

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", ping, name="ping"),
    path('api/', include('accounts.urls')),
]
