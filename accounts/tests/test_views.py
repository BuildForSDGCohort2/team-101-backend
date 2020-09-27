'''Module test cases for accounts/views.py'''

from django.urls import reverse
from django.contrib.auth import get_user_model

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


class ContributorTestCase(APITestCase):

    '''Test cases for contributor and maintainer views.'''
    def setUp(self):

        '''Initial setup'''
        self.client = APIClient()
        self.contributor = self.client.post('/api/auth/registration/', data={
            'first_name': 'contry',
            'last_name': 'user',
            'password1': 'passworddd1234',
            'password2': 'passworddd1234',
            'email': 'contry@example.com',
            'username': 'justme',
            'town_city': 'Ikeja',
            'state': 'Lagos',
            'country': 'NG'
        })

        self.contributor2 = self.client.post('/api/auth/registration/', data={
            'first_name': 'contry',
            'last_name': 'user',
            'password1': 'passworddd1234',
            'password2': 'passworddd1234',
            'email': 'contry@example.com',
            'username': 'justme',
            'town_city': 'Ikeja',
            'state': 'Lagos',
            'country': 'NG'
        })

        self.maintainer = self.client.post('/api/auth/registration/', data={
            'first_name': 'test',
            'last_name': 'user',
            'password1': 'passworddd1234',
            'password2': 'passworddd1234',
            'email': 'test@example.com',
            'username': 'na_play',
            'town_city': 'Ikeja',
            'state': 'Lagos',
            'country': 'NG'
        })
        # make user a contributor.
        self.user = get_user_model().objects.get(email='contry@example.com')
        self.user.is_contributor = True
        self.user.save()

        self.contrib2 = get_user_model().objects.get(email='contry@example.com')
        self.contrib2.is_contributor = True
        self.contrib2.save()

        self.response = self.client.post(reverse('rest_login'), data={
            'email': 'test@example.com',
            'password': 'passworddd1234',
        })

        self.token = self.response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)

    def test_contributor_can_be_blacklisted(self):
    
        '''Test contributor can blacklisted successfully by a maintainer.'''
        # make user a maintainer.
        maintainer = get_user_model().objects.get(email='test@example.com')
        maintainer.is_maintainer = True
        maintainer.save()

        data = {
            'contributor': self.user.id,
            'maintainer': maintainer.id,
            'reason': 'Fake account. Uploaded misleading info 3 times.',
        }
        response = self.client.post('/api/blacklist/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_contributor_fails_to_be_blacklisted(self):
    
        '''
        Test contributor cannot blacklisted if `user` type trying to 
        blacklist is NOT maintainer or admin.
        '''
        # does not assign a `user` type.
        not_maintainer = get_user_model().objects.get(email='test@example.com')

        data = {
            'contributor': self.user.id,
            'maintainer': not_maintainer.id,
            'reason': 'Fake account. Uploaded misleading info 3 times.'
        }

        response = self.client.post('/api/blacklist/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_maintainer_can_remove_contributor_from_blacklist(self):

        '''Test maintainer can delete a blacklist entry.'''
        maintainer = get_user_model().objects.get(email='test@example.com')
        maintainer.is_maintainer = True
        maintainer.save()

        data = {
            'contributor': self.contrib2.id,
            'maintainer': maintainer.id,
            'reason': 'Fake account. Uploaded misleading info 3 times.',
        }
        added_blacklist = self.client.post('/api/blacklist/', data=data)

        url = '/api/blacklist/' + str(added_blacklist.data['id']) +'/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_falis_remove_contributor_from_blacklist(self):

        '''Test non-maintainer or admin type cannot delete a blacklist entry.'''
        maintainer = get_user_model().objects.get(email='test@example.com')
        maintainer.is_maintainer = True
        maintainer.save()

        data = {
            'contributor': self.contrib2.id,
            'maintainer': maintainer.id,
            'reason': 'Fake account again.',
        }
        added_blacklist = self.client.post('/api/blacklist/', data=data)

        not_maintainer = get_user_model().objects.get(email='test@example.com')
        not_maintainer.is_maintainer = False
        not_maintainer.save()

        url = '/api/blacklist/' + str(added_blacklist.data['id']) +'/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
