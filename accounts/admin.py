from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import Follow, CustomUser as User

# Register your models here.
# Affichage standard
# admin.site.register(User) 

# Créez une classe personnalisée UserAdmin pour définir les champs que vous souhaitez afficher 
class CustomUserAdmin(BaseUserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_seen')

    # Champs à utiliser pour rechercher des utilisateurs
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Champs à utiliser pour filtrer la liste des utilisateurs
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Configuration des sections et des champs dans le formulaire de modification utilisateur
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'last_seen')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Configuration des sections et des champs dans le formulaire de création utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # Champs en lecture seule
    readonly_fields = ('last_login', 'date_joined', 'last_seen')

    # Champs de tri par défaut
    ordering = ('username',)

# Enregistrez votre modèle User avec votre nouvelle classe CustomUserAdmin :
admin.site.register(User, CustomUserAdmin)

# Affichage personnalisé
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to', 'created_at', 'get_follow_details', 'get_follow_count', 'get_follower_count')

    def get_follow_details(self, obj):
        # Ajoutez la logique nécessaire pour afficher les détails du suivi
        return f"{obj.user_from.get_username()} follows {obj.user_to.get_username()}"
    get_follow_details.short_description = 'Follow Details'

    def get_follow_count(self, obj):
        return obj.user_from.following.count()  # Nombre d'utilisateurs que user_from suit
    get_follow_count.short_description = 'Follow Count'

    def get_follower_count(self, obj):
        return obj.user_to.followers.count()  # Nombre d'utilisateurs qui suivent user_to
    get_follower_count.short_description = 'Follower Count'
    