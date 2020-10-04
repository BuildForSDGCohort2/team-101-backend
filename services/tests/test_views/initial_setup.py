'''Common functions shared between views test.'''
from django.contrib.auth import get_user_model

def make_maintainer():

    '''Function to switch to `contributor` type'''
    pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
    pseudo_maintainer.is_maintainer = True
    pseudo_maintainer.is_contributor = False
    pseudo_maintainer.save()

def make_contributor():

    '''Function to switch to `maintainer` type'''
    pseudo_maintainer = get_user_model().objects.get(email='contry@example.com')
    pseudo_maintainer.is_maintainer = False
    pseudo_maintainer.is_contributor = True
    pseudo_maintainer.save()
