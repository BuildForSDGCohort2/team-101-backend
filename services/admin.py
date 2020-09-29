from django.contrib import admin
import services.models as models

admin.site.register((
    models.Category,
    models.Item,
    models.ReservedItemRequest,
    models.UserItemRequest,
    models.Tag,
))
