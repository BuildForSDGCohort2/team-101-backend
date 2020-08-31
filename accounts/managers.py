'''
This module creates a custom manager which overrides `Model.objects` method to allow email as username field.
'''
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomManager(BaseUserManager):
    ''' Custom Manager '''
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        if not email or not password:
            raise ValueError('Email and password are required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_contributor(self, email, password=None, **extra_fields):
        '''Create and save a contributor with the given email and password.'''

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_maintainer', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_maintainer(self, email, password, **extra_fields):
        ''' Create and saves a maintainer with given email and password.'''
        
        extra_fields.setdefault('is_maintainer', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        '''Create and save a SuperUser with the given email and password.'''

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
