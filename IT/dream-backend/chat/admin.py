from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Message)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'author')