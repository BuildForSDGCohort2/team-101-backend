'''Test cases for Services item View'''
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from services.models import Category
from .initial_setup import make_maintainer


class ItemTestCase(APITestCase):

    '''Item test case'''
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

        self.maintainer = get_user_model().objects.get(email='test@example.com')
        self.contrib2 = get_user_model().objects.get(email='contry@example.com')
        self.category = Category.objects.create(name='Schools')

    def create_file(self, added_by):

        '''Create sample file for upload'''
        return {
            'name':'simple file',
            'category': self.category.id,
            'desciption': 'Dataset for schools in Aguda, Surulere.',
            'resource': SimpleUploadedFile('sch_aguda.csv', b'name,location,number', 'text/csv'),
            'added_by': added_by
        }

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

    def logout(self):

        '''Logout function for client'''
        self.client.logout()

    def test_maintainer_can_create_item(self):

        '''Test maintainer or admin can create item'''
        self.maintainer_login()
        response = self.client.post('/api/services/item/',
        data=self.create_file(self.maintainer.id))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_contributor_can_create_item(self):

        '''Test contributor can create an item'''
        self.contributor_login()
        response = self.client.post('/api/services/item/', data=self.create_file(self.contrib2.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_contributor_can_get_item(self):

        '''Test contributor can get a item'''
        self.contributor_login()
        response = self.client.get('/api/services/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_can_get_item(self):

        '''Test anonymous user can get a item'''
        response = self.client.get('/api/services/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_fails_create_item(self):

        '''Test anonymous user cannot create a item'''
        response = self.client.post('/api/services/item/', data={'name': 'Agriculture'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_file_owner_cannot_delete_item(self):

        '''Test non-file owner cannot delete another user's item'''
        self.maintainer_login()
        item = self.client.post('/api/services/item/', data=self.create_file(self.maintainer.id))

        self.logout()
        self.contributor_login()
        response = self.client.delete('/api/services/item/' + str(item.data['id']) + '/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_file_owner_can_delete_item(self):

        '''Test file owner/uploader can delete item'''
        self.maintainer_login()
        item = self.client.post('/api/services/item/', data=self.create_file(self.maintainer.id))

        response = self.client.delete('/api/services/item/' + str(item.data['id']) + '/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_maintainer_can_update_item(self):

        '''Test maintainer or admin can edit/update item'''
        self.maintainer_login()
        item = self.client.post('/api/services/item/', data=self.create_file(self.maintainer.id))
        url = '/api/services/item/' + str(item.data['id']) + '/'

        data = self.create_file(self.maintainer.id)
        data['name'] = 'Minor change'
        data['updated_by'] = self.contrib2.id

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_fails_update_item(self):

        '''Test anonymous user cannot update/edit a item'''
        self.contributor_login()
        make_maintainer()

        item = self.client.post('/api/services/item/', data=self.create_file(self.maintainer.id))
        url = '/api/services/item/' + str(item.data['id']) + '/'

        self.client.logout()
        response = self.client.put(url, data=self.create_file(''))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
