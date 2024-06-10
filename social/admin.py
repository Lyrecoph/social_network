from django.contrib import admin
from social.models import Notification
# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'read', 'created', 'updated')