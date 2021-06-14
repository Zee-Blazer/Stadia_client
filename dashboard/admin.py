from django.contrib import admin
from . import models


@admin.register(models.Event)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'name', 'capacity', 'date'
    search_fields = 'name',
