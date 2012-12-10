from django.contrib import admin
from message.models import Broadcast

class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')

admin.site.register(Broadcast, BroadcastAdmin)
