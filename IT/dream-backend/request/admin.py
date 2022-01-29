from django.contrib import admin
from . import models


# This part deals with what can be seen from the admin administration portal
# add possibility in admin console to create new models
@admin.register(models.HelpRequest)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'status', 'author','receiver')


@admin.register(models.TipRequest)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('proposed_title', 'proposed_tip', 'status', 'slug')