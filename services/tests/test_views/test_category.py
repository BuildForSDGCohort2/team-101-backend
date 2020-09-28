'''Test cases for Services Category View'''
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


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
        # make user a contributor.
        self.user = get_user_model().objects.get(email='contry@example.com')
        self.contrib2 = get_user_model().objects.get(email='contry@example.com')
        
    def test_maintainer_can_create_category(self):

        '''Test maintainer or admin can create category'''
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

        response = self.client.post('/api/services/category/', data={'name': 'Technology'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_contributor_fails_create_category(self):

        '''Test contributor cannot create a category'''
        login = self.client.post(reverse('rest_login'), 
            data={
                'email': 'contry@example.com',
                'password': 'passworddd1234',
            })
        token = login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        response = self.client.post('/api/services/category/', data={'name': 'Technology'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contributor_can_get_category(self):

        '''Test contributor can get a category'''
        login = self.client.post(reverse('rest_login'), data={
            'email': 'contry@example.com',
            'password': 'passworddd1234',
        })
        token = login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        response = self.client.get('/api/services/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_can_get_category(self):

        '''Test anonymous user can get a category'''
        response = self.client.get('/api/services/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_fails_get_category(self):
    
        '''Test anonymous user cannot create a category'''
        response = self.client.post('/api/services/category/', data={'name': 'Agriculture'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_maintainer_can_delete_category(self):

        '''Test maintainer or admin can delete category'''
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

        category = self.client.post('/api/services/category/', data={'name': 'Technology'})
        response = self.client.delete('/api/services/category/' + str(category.data['id']) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_contributor_fails_delete_category(self):

        '''Test contributor cannot delete a category'''
        login = self.client.post(reverse('rest_login'), data={
            'email': 'contry@example.com',
            'password': 'passworddd1234',
        })
        token = login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
        pseudo_maintainer.is_maintainer = True
        pseudo_maintainer.is_contributor = False
        pseudo_maintainer.save()

        category = self.client.post('/api/services/category/', data={'name': 'Technology'})

        pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
        pseudo_maintainer.is_maintainer = False
        pseudo_maintainer.is_contributor = True
        pseudo_maintainer.save()

        response = self.client.delete('/api/services/category/' + str(category.data['id']) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_fails_delete_category(self):

        '''Test anonymous user cannot delete a category'''
        login = self.client.post(reverse('rest_login'), data={
            'email': 'contry@example.com',
            'password': 'passworddd1234',
        })
        token = login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
        pseudo_maintainer.is_maintainer = True
        pseudo_maintainer.is_contributor = False
        pseudo_maintainer.save()

        category = self.client.post('/api/services/category/', data={'name': 'Technology'})

        self.client.logout()
        response = self.client.delete('/api/services/category/' + str(category.data['id']) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_maintainer_can_update_category(self):
    
        '''Test maintainer or admin can edit/update category'''
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

        category = self.client.post('/api/services/category/', data={'name': 'Technology'})
        url = '/api/services/category/' + str(category.data['id']) + '/'

        response = self.client.put(url, data={'name': 'changed Tech'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contributor_fails_update_category(self):

        '''Test contributor cannot update/edit a category'''
        login = self.client.post(reverse('rest_login'), data={
            'email': 'contry@example.com',
            'password': 'passworddd1234',
        })
        token = login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
        pseudo_maintainer.is_maintainer = True
        pseudo_maintainer.is_contributor = False
        pseudo_maintainer.save()

        category = self.client.post('/api/services/category/', data={'name': 'Technology'})

        pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
        pseudo_maintainer.is_maintainer = False
        pseudo_maintainer.is_contributor = True
        pseudo_maintainer.save()

        url = '/api/services/category/' + str(category.data['id']) + '/'
        response = self.client.put(url, data={'name': 'not gonna work'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_fails_update_category(self):

        '''Test anonymous user cannot update/edit a category'''
        login = self.client.post(reverse('rest_login'), data={
            'email': 'contry@example.com',
            'password': 'passworddd1234',
        })
        token = login.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
        pseudo_maintainer.is_maintainer = True
        pseudo_maintainer.is_contributor = False
        pseudo_maintainer.save()

        category = self.client.post('/api/services/category/', data={'name': 'Technology'})
        url = '/api/services/category/' + str(category.data['id']) + '/'

        self.client.logout()
        response = self.client.put(url, data={'name': 'not gonna work.'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
