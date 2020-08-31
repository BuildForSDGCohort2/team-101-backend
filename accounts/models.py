'''
This module handles all user accounts types:
- `contributor`
- `maintainer`
- `super user` or overall admin.
'''
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from accounts.managers import CustomManager


class User(AbstractBaseUser, PermissionsMixin):
    ''' Custom user model '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.Charfield(max_length=60, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    first_name = models.CharField(max_length=250, null=False, blank=False)
    last_name = models.CharField(max_length=250, null=False, blank=False)
    phone_number = PhoneNumberField(blank=True, null=True, help_text='Eg +234, +233')
    town_city = models.TextField(help_text='Enter residing city or town')
    state = models.CharField(max_length=50)
    country = CountryField(blank_label='(select country)', multiple=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_maintainer = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name +' '+ self.last_name

    def get_short_name(self):
        return self.first_name

