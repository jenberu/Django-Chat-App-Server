from django.contrib import admin
from .models import Room,Message


# Register your models here.
admin.site.register(Room)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
 list_display = ['sent_on', 'user', 'room', 'content']
 list_filter = ['sent_on', 'room']
 search_fields = ['content']
 raw_id_fields = ['user']