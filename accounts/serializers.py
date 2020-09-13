from rest_framework import serializers


from dj_rest_auth.registration.serializers import RegisterSerializer

from .models import User



class CustomRegisterSerializer(RegisterSerializer, serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'town_city', 'state', 'country']
    
    def save(self, request):
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            password=self.validated_data['password1'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            town_city=self.validated_data['town_city'],
            state=self.validated_data['state'],
            country = self.validated_data['country']
        )
        password2 = self.validated_data['password2']
        
        user.set_password(password2)
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'town_city', 'state', 'country', 'is_maintainer']

