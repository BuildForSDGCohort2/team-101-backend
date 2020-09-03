from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

import services.models as models
from accounts.models import User


class ModelTestCase(TestCase):
    '''Models test for `services` app'''
    def setUp(self):
        file_pdf = SimpleUploadedFile('play.pdf', b'file_content', content_type='application/pdf')
        file = SimpleUploadedFile('joke.doc', b'I have no idea what I am writing:)', content_type='text/plain')
        self.contributor = User.objects.create_contributor(
            username='testy',
            email='contributor@gmail.com',
            password='passtest',
            first_name='contribe',
            last_name='author',
            town_city='Garki',
            state='Abuja',
            country='NG',
        )
        self.category = models.Category.objects.create(name='Technology')
        self.tag1 = models.Tag.objects.create(name='mobile phones')

        self.item1 = models.Item.objects.create(
            name='Mobile phone users in Abeokuta',
            category=self.category,
            size=3.4,
            file_type='pdf',
            description='An excel sheet containing all counts of mobile phones',
            resource = file,
            added_by=self.contributor
        )

        self.user_request_item = models.UserItemRequest.objects.create(
            item_name='Schools in Edo',
            item_description='I would like a spreadsheet of the school in Benin-North.',
            requester_email='test@gmail.com',
            requester_name='Anika',
        )

        self.request_reserved_item = models.ReservedItemRequest.objects.create(
            item=self.item1,
            organization_name='Hungry man limited',
            organization_email='hungrynigerian@gmail.com',
            rep_name='lion',
            reason='I want to steal all there phones',
        )
    
    def test_category_was_created(self):
        response = models.Category.objects.get(name='Technology')
        self.assertEqual(response.id, 1)
    
    def test_category_can_be_updated(self):
        response = models.Category.objects.get(id=1)
        response.name = 'Oil and Gas'
        response.save()
        self.assertEqual(response.name, 'Oil and Gas')
    
    def test_category_can_be_deleted(self):
        category = models.Category.objects.get(id=1)
        category.delete()
        all_categories = models.Category.objects.all()
        self.assertEqual(all_categories.count(), 0)
    
    def test_item_was_created(self):
        response = models.Item.objects.get(category=self.category)
        self.assertEqual(response.file_type, 'pdf')
    
    def test_item_can_be_updated(self):
        response = models.Item.objects.get(name='Mobile phone users in Abeokuta')
        response.name = 'Telephone'
        response.save()
        self.assertEqual(response.name, 'Telephone')
    
    def test_item_can_be_deleted(self):
        item = models.Item.objects.get(name='Mobile phone users in Abeokuta')
        item.delete()
        all_items = models.Item.objects.all()
        self.assertEqual(all_items.count(), 0)
    
    def test_user_can_request_item(self):
        request = models.UserItemRequest.objects.all()
        self.assertEqual(request.count(), 1)
    
    def test_user_can_request_item(self):
        request = models.ReservedItemRequest.objects.all()
        self.assertEqual(request.count(), 1)
