from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class RegistrationTest(APITestCase):
    """
    Ensure we can create a new user
    by registering & also login using the same user
    """
    data = {
            "username": "jdoe",
            "email": "john.doe@gmail.com",
            "password1": "password!!!",
            "password2": "password!!!",
            "first_name": "John",
            "last_name": "Doe",
            "town_city": "Lugbe",
            "state": "Abuja",
            "country": "NG"
        }

    def test_create_user(self):
        url = reverse('rest_register')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {"detail": "Verification e-mail sent."})

    def test_login(self):

        user = User.objects.create(
            username=self.data['username'],
            email=self.data['email'],
            password=self.data['password1'],
            first_name=self.data['first_name'],
            last_name=self.data['last_name'],
            town_city=self.data['town_city'],
            state=self.data['state'],
            country=self.data['country']
        )
        user.set_password(self.data['password1'])
        user.save()
        response = self.client.login(email=self.data['email'],
                                     password=self.data['password1'])
        self.assertTrue(response)
