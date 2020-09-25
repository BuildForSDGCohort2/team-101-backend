'''Tests for each model in the services app.'''

from django.test import TestCase

import accounts.models as models


class ModelsTestCase(TestCase):

    '''Test model creations in app.'''
    def setUp(self):

        '''Initial setup'''
        self.contributor = models.User.objects.create_contributor(
            username='testy',
            email='contributor@gmail.com',
            password='passtest',
            first_name='contribe',
            last_name='author',
            town_city='Garki',
            state='Abuja',
            country='NG',
        )
        self.maintainer = models.User.objects.create_maintainer(
            username='mainty',
            email='maintainer@gmail.com',
            password='passtest',
            first_name='mainty',
            last_name='checker',
            town_city='Salema',
            state='Accra',
            country='GH',
        )
        self.superuser = models.User.objects.create_superuser(
            username='admin',
            email='superuser@gmail.com',
            password='passtest',
            first_name='addy',
            last_name='oga',
            town_city='boungee',
            state='Johannesburg',
            country='SA',
        )
        self.blacklist = models.BlacklistContributor.objects.create(
            contributor=self.contributor,
            maintainer=self.maintainer,
            reason='Fake account'
        )
        self.contributor_request = models.ContributorRequest.objects.create(
            first_name='new contribe',
            email='new@gmail.com'
        )

    def test_contributor_was_created(self):

        '''Test contributor creation'''
        response = models.User.objects.get(email='contributor@gmail.com', is_maintainer=False)
        self.assertEqual(response.email, 'contributor@gmail.com')

    def test_maintainer_was_created(self):

        '''Test maintainer creation'''
        response = models.User.objects.get(
            email='maintainer@gmail.com',
            is_maintainer=True,
            is_superuser=False
        )
        self.assertEqual(response.email, 'maintainer@gmail.com')

    def test_superuser_was_created(self):

        '''Test admin/super user creation'''
        response = models.User.objects.get(
            email='superuser@gmail.com',
            is_maintainer=False,
            is_superuser=True
        )
        self.assertEqual(response.email, 'superuser@gmail.com')

    def test_contributor_can_be_updated(self):

        '''Test contributor detail edit'''
        response = models.User.objects.get(email='contributor@gmail.com', is_maintainer=False)
        response.first_name = 'Wazobia'
        response.save()

        self.assertEqual(response.first_name, 'Wazobia')

    def test_maintainer_can_be_updated(self):

        '''Test maintainer detail edit'''
        response = models.User.objects.get(
            email='maintainer@gmail.com',
            is_maintainer=True,
            is_superuser=False
        )
        response.last_name = 'Chicken'
        response.save()

        self.assertEqual(response.last_name, 'Chicken')

    def test_superuser_can_be_updated(self):

        '''Test admin/super user detail edit'''
        response = models.User.objects.get(
            email='superuser@gmail.com',
            is_maintainer=False,
            is_superuser=True
        )
        response.state = 'Borno'
        response.save()

        self.assertEqual(response.state, 'Borno')

    def test_user_can_be_deleted(self):

        '''Test `user` deletion.'''
        user = models.User.objects.get(email='maintainer@gmail.com')
        user.delete()
        all_users = models.User.objects.count()

        self.assertEqual(all_users, 2)

    def test_contributor_was_blacklisted(self):

        '''Test `contributor` user type can be blacklisted'''
        response = models.BlacklistContributor.objects.all()
        self.assertEqual(response.count(), 1)

    def test_contributor_request_was_created(self):

        '''Test site visitor can request to become a contributor.'''
        response = models.ContributorRequest.objects.all()
        self.assertEqual(response.count(), 1)
