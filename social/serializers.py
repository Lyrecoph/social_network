# from django.contrib.auth.models import User
from accounts.models import CustomUser as User
from rest_framework.serializers import ModelSerializer, RelatedField

from social.models import Notification, Post, Comment

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class TargetSerializer(RelatedField):

    def to_representation(self, value):
        return value.content

    # def to_representation(self, value):
    #     if isinstance(value, Post):
    #         return f"Publication: {value.content[:30]}..."  # Ou autre champ pertinent
    #     elif isinstance(value, Comment):
    #         return f"Commentaire: {value.content[:30]}..."  # Ou autre champ pertinent
    #     # return str(value)  # Si c'est un autre type


class NotificationSerializer(ModelSerializer):
    # user = UserSerializer(read_only=True)
    target = TargetSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'read', 'user', 'target', 'created', 'action']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = {'username': instance.user.username, 'id': instance.user.id}  # Correction ici
        # data['target'] = str(instance.target) if instance.target else None
        return data
        