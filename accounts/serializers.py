from django.contrib.auth import get_user_model

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer

from .models import BlacklistContributor


class CustomRegisterSerializer(RegisterSerializer, serializers.ModelSerializer):

    '''Custom serializer to handle registration'''
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'password1',
            'password2', 'first_name', 'last_name',
            'town_city', 'state', 'country'
        ]

    def save(self, request):
        user = get_user_model().objects.create_contributor(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            password=self.validated_data['password1'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            town_city=self.validated_data['town_city'],
            state=self.validated_data['state'],
            country=self.validated_data['country']
        )
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):

    '''Custom `user` detail serializer'''
    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'town_city', 'state',
            'country', 'is_maintainer'
        ]
        read_only_fields = ('email',)


class BlacklistSerializer(serializers.ModelSerializer):

    '''Serializer for blacklisting contributors.'''
    class Meta:
        model = BlacklistContributor
        fields = '__all__'
