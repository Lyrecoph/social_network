from django.contrib import admin
from tchat.models import Conversation, Message

# Register your models here.

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_online_users')

    def get_online_users(self, obj):
        return ", ".join([user.username for user in obj.online.all()])
    get_online_users.short_description = 'Utilisateurs en ligne'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'content', 'from_user', 'to_user', 'created_at', 'read', 'is_edited')
    
    


