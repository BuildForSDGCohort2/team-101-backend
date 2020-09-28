from rest_framework import serializers

import services.models as model


class CategorySerializer(serializers.ModelSerializer):

    '''Category serializer'''
    class Meta:
        model = model.Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    '''Tag serializer'''
    class Meta:
        model = model.Tag
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    '''Dataset(item) serializer'''
    class Meta:
        model = model.Item
        fields = '__all__'


class UserItemRequestSerializer(serializers.ModelSerializer):

    '''Anonymous/visting user dataset(item) request serializer'''
    class Meta:
        model = model.UserItemRequest
        fields = '__all__'


class ReservedItemRequestSerializer(serializers.ModelSerializer):

    '''Reserved dataset(item) request serializer'''
    class Meta:
        model = model.ReservedItemRequest
        fields = '__all__'
