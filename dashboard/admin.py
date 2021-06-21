from django.contrib import admin
from . import models


@admin.register(models.Event)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'event_creator', 'name', 'capacity', 'date'
    search_fields = 'name',
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Ticket)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'attendee', 'event', 'book_seat'
    search_fields = 'event', 'attendee'
