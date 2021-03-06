from django.contrib import admin

from eventtracker.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['event', 'timestamp', 'params']
    list_filter = ['event', 'timestamp']

admin.site.register(Event, EventAdmin)
