from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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
    
