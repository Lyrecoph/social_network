from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'content', 'from_user', 'to_user', 'read')

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['to_user'] = {'username': instance.to_user.username, 'id': instance.to_user.id}  # Correction ici
        # data['target'] = str(instance.target) if instance.target else None
        data['from_user'] = {'username': instance.from_user.username, 'id': instance.from_user.id} 
        return data