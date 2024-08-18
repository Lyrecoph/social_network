from django.contrib import admin
from social.models import Notification, Post, LikeComment, LikePost, Comment

# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'read', 'created', 'updated')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'owner', 'get_users_like')
    
    def get_users_like(self, obj):
        return ", ".join([user.username for user in obj.users_like.all()])
    get_users_like.short_description = 'Users Like'

@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ('post', 'owner', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'content', 'owner', 'get_users_like')
    
    # La méthode get_users_like récupère tous les utilisateurs qui aiment le post ou le commentaire, 
    # et les affiche sous forme de chaîne de caractères séparée par des virgules.
    def get_users_like(self, obj):
        return ", ".join([user.username for user in obj.users_like.all()])
    get_users_like.short_description = 'Users Like'

@admin.register(LikeComment)
class LikeCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'owner', 'created_at')
