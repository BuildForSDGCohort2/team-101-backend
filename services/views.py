from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

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
        Get all tags
    create:
        Add a tag.
    read:
        Retrieve a tag.
    update:
        Update an existing tag.
    partial_update:
        Make patch update to an existing tag.
    delete:
        Delete a tag.
    '''
    queryset = model.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [permission.IsMaintainerOrReadOnly, permissions.AllowAny]


class ItemViewset(viewsets.ModelViewSet):

    '''
    list:
        Get all datasets flagged `is_active` for vistors(anonymous user).
        Get all datasets whether `is_active` or not for authenticated user type.
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
        Delete a dataset as `owner` or `admin`.
    '''
    serializer_class = serializers.ItemSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['name', 'created_at']
    search_fields = ['$name', '$created_at']
    ordering_fields = ['name','created_at']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return model.Item.objects.all()
        return model.Item.objects.filter(is_active=True)

    def destroy(self, request):
        dataset = self.get_object()
        if dataset.added_by == self.request.user:
            self.perform_destroy(dataset)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={'You are not authorized to perform this action'},
            status=status.HTTP_401_UNAUTHORIZED)
