from django.contrib import admin
from . import models


# This part deals with what can be seen from the admin administration portal
# add possibility in admin console to create new models
@admin.register(models.Question)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'area') #it is the field that appears in the admin list of questions


admin.site.register(models.Category)
