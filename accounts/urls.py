from django.urls import path, include, re_path

from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework.routers import DefaultRouter

import accounts.views as views

router = DefaultRouter()
router.register('blacklist', views.BlacklistViewset, basename='blacklist')

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls'), name='registration'),
    path('auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^auth/account-confirm-email/(?P<key>[-:\w]+)/$', views.EmailConfirmationView.as_view(), name='account_confirm_email'),
] + router.urls
