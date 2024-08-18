from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from accounts.models import CustomUser as User
# User = get_user_model()

# Create your models here.

class CreationModificationMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # lorsqu'on définit une classe dans une classe on parle de inner classe
    class Meta:
        abstract = True
        # ordering prend comme valeur un itérable(liste ou dictionnaire)
        # ordering nous permet à chaque fois que nous allons récupérer 
        # les données de notre DB elle seront ordonnées
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

# Génère la table publication
class Post(CreationModificationMixin):
    # null: True autorise les champs vides intervient plus au niveau de l'enregistrement de la DB
    # blank:True intervient plus au niveau de la validation du formulaire
    content = models.TextField(null=True)
    # slug = models.SlugField(max_length=500, unique=True)
    # image = models.ImageField(upload_to='images/post')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    # Une relation ManyToMany vers le modèle utilisateur pour représenter les utilisateurs
    # qui aiment la publication. Une relation ManyToMany vers le modèle utilisateur pour
    # représenter les utilisateurs qui aiment la publication.
    users_like = models.ManyToManyField(User, related_name='post_like', through='LikePost')
    
    # class Meta(CreationModificationMixin.Meta):
    #     indexes = [models.Index(fields=['slug'])]
        
    def __str__(self):
        return self.content

# Génère un table chargé d'ajouter les images
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_media')
    image = models.ImageField(upload_to='images/post/')
    created_at = models.DateTimeField(auto_now_add=True)
    
           
# Génère la table commentaire  
class Comment(CreationModificationMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    content = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    users_like = models.ManyToManyField(User, related_name='comment_like', through='LikeComment')
    
    def __str__(self) -> str:
        return self.content
    
    
# Le modèle LikePost est un modèle intermédiaire qui représente les "likes" des publications.
# Il relie les utilisateurs aux publications qu'ils aiment.
class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like_post')
    created_at = models.DateTimeField(auto_now_add=True)
    
    

class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_like')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like_comment')
    created_at = models.DateTimeField(auto_now_add=True)
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notified')
    action = models.CharField(max_length=255)
    # indique si la notification a été lu ou pas
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='obj', null=True, blank=True)
    # sert à sauvegarder l'id de l'objet recupérer
    object_id = models.IntegerField(null=True, blank=True)
    # associe l'object et son id
    target = GenericForeignKey('content_type', 'object_id')

    # optimisation des requêtes
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created']), models.Index(fields=['content_type', 'object_id'])]

    # def __str__(self):
    #     if self.content_type:
    #         return f"{self.user.username} - {self.action} on {self.content_type.model}"
    #     return f"{self.user.username} - {self.action}"
    
    def __str__(self):
        return f"{self.user.username} - {self.action} on {self.content_type.model}"


