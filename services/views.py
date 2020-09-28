from rest_framework import viewsets, permissions

import services.serializers as serializers
import services.models as model
import utils.permissions as permission

class CategoryViewset(viewsets.ModelViewSet):
    queryset = model.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permission.IsMaintainerOrReadOnly, permissions.AllowAny]


class TagViewset(viewsets.ModelViewSet):
    queryset = model.Category.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [permission.IsMaintainerOrReadOnly, permissions.AllowAny]
