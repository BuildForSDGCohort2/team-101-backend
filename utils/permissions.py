'''Custom API permission file.'''
from rest_framework import permissions


class IsMaintainerOrAdmin(permissions.BasePermission):

    '''View-level permission to only allow maintainers or admins.'''
    def has_permission(self, request, view):
        message = 'You are not authorized to this view'

        return request.user.is_maintainer or request.user.is_superuser


class IsMaintainerOrReadOnly(permissions.BasePermission):

    '''View-level permission to only allow maintainers or admins.'''
    def has_permission(self, request, view):
        message = 'You are not authorized to this view'
        
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return request.user.is_maintainer or request.user.is_superuser
        except AttributeError:  # Capture Anonymous user type
            return False

class IsFileOwnerOrAccessible(permissions.BasePermission):

    '''
    Object-level permission to only allow files flagged
    `is_accessible` to be seen by everyone.
    '''
    def has_object_permission(self, request, view, obj):
        message = 'File is not publically accessible.'

        return obj.owner == request.user or obj.is_accessible

class IsFileOwnerOrReadOnly(permissions.BasePermission):

    '''Object-level permission to only allow owners of a file to edit it.'''
    def has_object_permission(self, request, view, obj):
        message = 'Making changes to this file is not allowed.'

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
