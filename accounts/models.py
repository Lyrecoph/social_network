from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

# Création d'une classe abstraite avec le champ ManyToManyField
class UserFollow(models.Model):
    follow_user = models.ManyToManyField('self', through='Follow', related_name='followed', symmetrical=False)
    

    class Meta:
        abstract = True

# Créez un modèle CustomUser qui étend AbstractUser et UserFollow :
class CustomUser(AbstractUser, UserFollow):
    last_seen = models.DateTimeField(null=True, blank=True)

    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save()
    
    def online_status(self):
        return 'online' if self.is_online else 'offline'

    # Vous pouvez ajouter une méthode pour vérifier si l'utilisateur est en ligne
    def is_online(self):
        return any(conv.is_user_online(self) for conv in self.conversation_set.all())

    
# Ce modèle définit une relation de suivi (follow) entre les utilisateurs
class Follow(models.Model):
    # user_from est l'utilisateur qui suit
    user_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")
    # user_to est l'utilisateur suivi (utilisateur actuel)
    user_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['-created_at'])]
        # La déclaration unique_together = ('user_from', 'user_to') garantit que la combinaison 
        # des champs user et followed_user doit être unique. Cela signifie qu'un utilisateur (user_from) 
        # ne peut pas suivre un autre utilisateur (user_to) plus d'une fois.
        unique_together = ('user_from', 'user_to')

    def __str__(self):
        return "%s started following %s" % (self.user_from.get_username(), self.user_to.get_username())

# Cette ligne ajoute un champ many-to-many au modèle User pour permettre aux utilisateurs de suivre 
# d'autres utilisateurs. symmetrical=False indique que la relation de suivi n'est pas symétrique
# (si A suit B, cela ne signifie pas que B suit A)
# through=Follow permet d'utiliser la table follow comme une table intermediaire
# User.add_to_class('follow_user', models.ManyToManyField('self', through='Follow', related_name='followed', symmetrical=False))

