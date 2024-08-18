from asgiref.sync import sync_to_async

from django.db import models
from accounts.models import CustomUser as User

# Create your models here.
class Conversation(models.Model):
    name = models.CharField(max_length=100)
    # spécifie que plusieurs utilisateurs peuvent être en ligne au même moment
    online = models.ManyToManyField(to=User, blank=True)

    def __str__(self):
        return self.name
    
    
    # ajoute les utilisateurs de la liste des utilisateurs en ligne
    def join(self, user):
        self.online.add(user)
        self.save()
        print(f"{user.username} a rejoint la conversation {self.name}")

    
    # supprime les utilisateurs de la liste des utilisateurs en ligne
    def leave(self, user):
        self.online.remove(user)
        user.update_last_seen()
        self.save()
        print(f"{user.username} a quitté la conversation {self.name}")

    
    # compter le nombre d'utilisateur connecté
    def get_online_count(self):
        return self.online.count()
    
    
    # méthode pour vérifier si un utilisateur spécifique est en ligne
    def is_user_online(self, user):
        # return self.online.filter(id=user.id).exists()
        is_online = user in self.online.all()
        print(f"Vérification si {user.username} est en ligne: {is_online}")
        return is_online

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    # celui qui envoie le message
    from_user = models.ForeignKey(User, related_name='msg_from_me', on_delete=models.CASCADE)
    # celui qui reçoit le message
    to_user = models.ForeignKey(User, related_name='msg_to_me', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # par défaut les messages ne sont pas lu
    read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f'From {self.from_user.username} to {self.to_user.username}: {self.content}'