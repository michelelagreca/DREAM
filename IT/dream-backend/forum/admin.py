from django.contrib import admin
from . import models

# This part deals with what can be seen from the admin administration portal
# add possibility in admin console to create new models

admin.site.register(models.Category)


@admin.register(models.Question)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'area')


@admin.register(models.Tip)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'area', 'is_star')


@admin.register(models.Answer)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'likes', 'dislikes')
