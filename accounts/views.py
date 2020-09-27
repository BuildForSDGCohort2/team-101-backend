from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from rest_framework import status, viewsets, parsers
from rest_framework.response import Response
from dj_rest_auth.registration.views import VerifyEmailView

import accounts.serializers as serializers
import accounts.models as models
from utils.permissions import IsMaintainerOrAdmin


class EmailConfirmationView(VerifyEmailView):

    '''Email Confirmation view'''
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        user = confirmation.email_address.user
        if user.is_verified:
            return Response(
                {'detail':_('Email already verified')},
                status = status.HTTP_200_OK
            )
            #return Response({'detail': _('Email already verified')}, status=status.HTTP_200_OK)
        else:
            user.is_verified = True
            user.save()
            return Response(
                {'detail': _(user.username+ ' Mail Successfully Verified')}, 
                status=status.HTTP_200_OK
            )


class BlacklistViewset(viewsets.ModelViewSet):
    '''
    list:
        Get all entries in database as an admin user type.
    create:
        Blacklist a contributor.
    read:
        Retrieve a blacklisted entry.
    update:
        Update an existing entry.
    partial_update:
        Make patch update to an existing entry.
    delete:
        Delete an entry.
    '''
    queryset = models.BlacklistContributor.objects.all()
    serializer_class = serializers.BlacklistSerializer
    permission_classes = [IsMaintainerOrAdmin,]
