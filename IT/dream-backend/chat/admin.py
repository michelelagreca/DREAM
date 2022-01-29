from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.HrMessage)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'body', 'reference_hr')
