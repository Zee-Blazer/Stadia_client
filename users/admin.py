from django.contrib import admin
from . import models


@admin.register(models.UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'user', 'email'
    search_fields = 'email', 'user'
