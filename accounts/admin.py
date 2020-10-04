import csv
from django.http import HttpResponse
from django.contrib import admin

from accounts.models import User, BlacklistContributor, ContributorRequest


class ExportCsvMixin:
    '''Mixin for exporting as CSV file.'''
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
    
        return response
    export_as_csv.short_description = 'Export Selected'


class AccountsAdmin(admin.ModelAdmin, ExportCsvMixin):
    '''Define admin model for custom User model.'''
    fieldsets = (
        (None, {
            'fields': (
            'email',
            'username',
            'first_name',
            'last_name',
            'town_city',
            'state',
            'country',
            'is_active',
            'is_staff',
            'is_maintainer',
            'is_superuser',
            'is_verified',
        )
        }),
        ('Advanced options', {
            'classes': ('collapse', 'extrapretty'),
            'fields': ('last_login',  'groups', 'user_permissions'),
        }),
    )
    list_per_page = 20
    list_display = ('email', 'username', 'first_name', 'is_maintainer', 'is_active',)
    list_filter = ('created_at', 'is_active', 'is_maintainer',)
    actions_on_bottom = True
    search_fields = ('email', 'first_name', 'last_name')
    actions = ('deactivate_user', 'activate_user', 'export_as_csv')

    def deactivate_user(self, request, queryset):
        '''Deactivate selected user accounts.'''
        rows_updated = queryset.update(is_active=False)
        if rows_updated == 1:
            message_bit = '1 user was'
        else:
            message_bit = '{} users were' .format(rows_updated)
        self.message_user(request, '{} successfully deactivated.'.format(message_bit))

    def activate_user(self, request, queryset):
        '''Activate selected user accounts.'''
        rows_updated = queryset.update(is_active=True)
        if rows_updated == 1:
            message_bit = '1 user was'
        else:
            message_bit = '{} users were'.format(rows_updated)
        self.message_user(request, '{} successfully activated.'.format(message_bit))

    deactivate_user.short_description = 'Deactivate selected'
    activate_user.short_description = 'Activate selected'

admin.site.register(User, AccountsAdmin,)
admin.site.register(BlacklistContributor)
admin.site.register(ContributorRequest)
