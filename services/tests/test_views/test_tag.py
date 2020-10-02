'''Test cases for Services tag View'''
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

def make_maintainer():

    '''Function to switch to `contributor` type'''
    pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
    pseudo_maintainer.is_maintainer = True
    pseudo_maintainer.is_contributor = False
    pseudo_maintainer.save()

def make_contributor():

    '''Function to switch to `maintainer` type'''
    pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
    pseudo_maintainer.is_maintainer = False
    pseudo_maintainer.is_contributor = True
    pseudo_maintainer.save()

class CategoryTestCase(APITestCase):

    '''Category test case'''
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

        self.user = get_user_model().objects.get(email='contry@example.com')
        self.contrib2 = get_user_model().objects.get(email='contry@example.com')

    def maintainer_login(self):

        '''Method for maintainer login'''
        maintainer = get_user_model().objects.get(email='test@example.com')
        maintainer.is_maintainer = True
        maintainer.is_contributor = False
        maintainer.save()

        login = self.client.post(reverse('rest_login'), data={
            'email': 'test@example.com',
            'password': 'passworddd1234',
        })
        token = login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

    def contributor_login(self):

        '''Method for contributor login'''
        login = self.client.post(reverse('rest_login'),
            data={
                'email': 'contry@example.com',
                'password': 'passworddd1234',
            })
        token = login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

    def test_maintainer_can_create_tag(self):

        '''Test maintainer or admin can create tag'''
        self.maintainer_login()
        response = self.client.post('/api/services/tag/', data={'name': 'Technology'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_contributor_fails_create_tag(self):

        '''Test contributor cannot create a tag'''
        self.contributor_login()
        response = self.client.post('/api/services/tag/', data={'name': 'Technology'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contributor_can_get_tag(self):

        '''Test contributor can get a tag'''
        self.contributor_login()
        response = self.client.get('/api/services/tag/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_can_get_tag(self):

        '''Test anonymous user can get a tag'''
        response = self.client.get('/api/services/tag/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_fails_get_tag(self):

        '''Test anonymous user cannot create a tag'''
        response = self.client.post('/api/services/tag/', data={'name': 'Agriculture'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_maintainer_can_delete_tag(self):

        '''Test maintainer or admin can delete tag'''
        self.maintainer_login()
        tag = self.client.post('/api/services/tag/', data={'name': 'Technology'})

        response = self.client.delete('/api/services/tag/' + str(tag.data['id']) + '/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_maintainer_can_get_tag(self):

        '''Test maintainer or admin can get tag'''
        self.maintainer_login()
        tag = self.client.post('/api/services/tag/', data={'name': 'Technology'})
        response = self.client.get('/api/services/tag/' + str(tag.data['id']) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contributor_fails_delete_tag(self):

        '''Test contributor cannot delete a tag'''
        self.contributor_login()
        make_maintainer()

        tag = self.client.post('/api/services/tag/', data={'name': 'Technology'})
        make_contributor()
        response = self.client.delete('/api/services/tag/' + str(tag.data['id']) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_fails_delete_tag(self):

        '''Test anonymous user cannot delete a tag'''
        self.contributor_login()
        make_maintainer()

        tag = self.client.post('/api/services/tag/', data={'name': 'Technology'})

        self.client.logout()
        response = self.client.delete('/api/services/tag/' + str(tag.data['id']) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_maintainer_can_update_tag(self):

        '''Test maintainer or admin can edit/update tag'''
        self.maintainer_login()
        tag = self.client.post('/api/services/tag/', data={'name': 'Technology'})
        url = '/api/services/tag/' + str(tag.data['id']) + '/'

        response = self.client.put(url, data={'name': 'changed Tech'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contributor_fails_update_tag(self):

        '''Test contributor cannot update/edit a tag'''
        self.contributor_login()
        make_maintainer()

        tag = self.client.post('/api/services/tag/', data={'name': 'Technology'})
        make_contributor()

        url = '/api/services/tag/' + str(tag.data['id']) + '/'
        response = self.client.put(url, data={'name': 'not gonna work'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_fails_update_tag(self):

        '''Test anonymous user cannot update/edit a tag'''
        self.contributor_login()
        make_maintainer()

        tag = self.client.post('/api/services/tag/', data={'name': 'Technology'})
        url = '/api/services/tag/' + str(tag.data['id']) + '/'

        self.client.logout()
        response = self.client.put(url, data={'name': 'not gonna work.'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
