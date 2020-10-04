from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_delete

from data_for_africa.settings import AUTH_USER_MODEL


class Category(models.Model):

    '''Category where all Datasets must belong.'''
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Tag(models.Model):

    '''Possible tags to Dataset.'''
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):

    '''Datasets model'''
    name = models.CharField(max_length=80, default='test')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    resource = models.FileField(upload_to='resources/')
    added_by = models.ForeignKey(AUTH_USER_MODEL, related_name='added_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(AUTH_USER_MODEL, related_name='updated_by',
    on_delete=models.CASCADE, blank=True, null=True)
    is_reserved = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} : {}'.format(self.name, self.category.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        # deletes old file when making an update to file
        try:
            old = Item.objects.get(id=self.id)
            if old.file != self.file:
                old.file.delete(save=False)
        except:
            pass
        super(Item, self).save(*args, **kwargs)

@receiver(post_delete, sender=Item)
def file_delete(sender, instance, **kwargs):
    '''Post_delete signal for deleting `Item` resource to prevent orphaned files'''
    instance.resource.delete(save=False)


class UserItemRequest(models.Model):

    '''Anonymous user requests for a dataset NOT currently found on the site.'''
    item_name = models.CharField(max_length=60)
    item_description = models.TextField()
    requester_email = models.EmailField()
    requester_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} item: {}'.format(self.requester_email, self.item_name)


class ReservedItemRequest(models.Model):

    '''Individual or organization requests reserved dataset model.'''
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=80)
    organization_email = models.EmailField()
    rep_name = models.CharField(max_length=50)
    reason = models.TextField(help_text='What will you use this dataset for?')
    is_approved = models.BooleanField(default=False, blank=True)
    is_pending = models.BooleanField(default=True, blank=True)
    is_rejected = models.BooleanField(default=False, blank=True)
    maintainer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'item: {}'.format(self.item.name)
