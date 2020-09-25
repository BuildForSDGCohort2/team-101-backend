'''Module test cases for accounts/views.py'''

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class UserTestCase(APITestCase):

    '''Test cases for user authentication views.'''
    def setUp(self):

        '''Initial setup'''
        self.client = APIClient()
        self.user = self.client.post('/api/auth/registration/', data={
            'first_name': 'test',
            'last_name': 'user',
            'password1': 'passworddd1234',
            'password2': 'passworddd1234',
            'email': 'test@example.com',
            'username': 'justme',
            'town_city': 'Ikeja',
            'state': 'Lagos',
            'country': 'NG'
        })

        self.response = self.client.post(reverse('rest_login'), data={
            'email': 'test@example.com',
            'password': 'passworddd1234',
        })
        self.token = self.response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)

    def test_user_login(self):

        '''Test user can login after registration.'''
        response = self.client.post(reverse('rest_login'), data={
            'email': 'test@example.com',
            'password': 'passworddd1234',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_login_with_wrong_credentials(self):

        '''Test fails with incorrect login credentials.'''
        response = self.client.post(reverse('rest_login'), data={
            'email': 'incorrect@example.com',
            'password': 'passworddd1234',
        })

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_retrieval(self):

        '''Test user can retrieve their details from url.'''
        data = {
            'email':'test@example.com'
        }
        response = self.client.get('/api/auth/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
