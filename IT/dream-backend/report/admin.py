from django.contrib import admin
from .models import HarvestReport


# This part deals with what can be seen from the admin administration portal
# add possibility in admin console to create new models
@admin.register(HarvestReport)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'date', 'id', 'status', 'slug', 'author')
    #prepopulated_fields = {'slug': ('title',), }

