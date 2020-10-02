from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser

import services.serializers as serializers
import services.models as model
import utils.permissions as permission

class CategoryViewset(viewsets.ModelViewSet):

    '''
    Category viewset.
    list:
        Get all categories.
    create:
        Add a category as a `maintainer` or `admin`.
    read:
        Retrieve a category.
    update:
        Update an existing category as a `maintainer` or `admin`.
    partial_update:
        Make patch update to an existing category as a `maintainer` or `admin`.
    delete:
        Delete a category as a `maintainer` or `admin`.
    '''
    queryset = model.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permission.IsMaintainerOrReadOnly, permissions.AllowAny]


class TagViewset(viewsets.ModelViewSet):

    '''
    list:
        Get only files belonging to particular `user`.
        Or get all files in database as an admin user type.
    create:
        Upload a file.
    read:
        Retrieve a file.
    update:
        Update an existing file.
    partial_update:
        Make patch update to an existing file.
    delete:
        Delete a file.
    '''
    queryset = model.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [permission.IsMaintainerOrReadOnly, permissions.AllowAny]


class ItemViewset(viewsets.ModelViewSet):

    '''
    list:
        Get all datasets flagged `is_active`.
    create:
        Upload a dataset as a `contributor`, `maintainer` or `admin`.
        Multiple tags can be added/removed. dataset should only belong to one category.
    read:
        Retrieve a dataset.
    update:
        Update an existing dataset as a `contributor`, `maintainer` or `admin`.
    partial_update:
        Make patch update to an existing dataset as a `contributor`, `maintainer` or `admin`.
    delete:
        Delete a dataset as `maintainer` or `admin`.
    '''
    queryset = model.Item.objects.filter(is_active=True)
    serializer_class = serializers.ItemSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [permission.IsMaintainerOrReadOnly, permissions.AllowAny]

    def get_parsers(self):

        '''To enable file uploads via Swagger API endpoint'''
        if getattr(self, 'swagger_fake_view', False):
            return [MultiPartParser]
        return super().get_parsers()
