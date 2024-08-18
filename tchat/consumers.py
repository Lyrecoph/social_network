import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from accounts.models import CustomUser as User
from tchat.models import Conversation, Message
from tchat.serializers import MessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.from_user = self.scope['user']
        self.conversation_name = self.scope['url_route']['kwargs']['username']
        self.conversation_name = f"chat_{self.conversation_name}"
        
        self.conversation, created = await sync_to_async(Conversation.objects.get_or_create)(name=self.conversation_name)
        
        if self.from_user.is_authenticated:
            await self.channel_layer.group_add(self.conversation_name, self.channel_name)
            await sync_to_async(self.conversation.join)(self.from_user)
            print(f"{self.from_user.username} connecté à la conversation {self.conversation_name}")
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.from_user.is_authenticated:
            await sync_to_async(self.conversation.leave)(self.from_user)
            await self.channel_layer.group_discard(self.conversation_name, self.channel_name)
            print(f"{self.from_user.username} déconnecté de la conversation {self.conversation_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        self.to_user = await self.get_receiver()

        message_instance = await sync_to_async(Message.objects.create)(
            conversation=self.conversation, 
            content=message,
            from_user=self.from_user,
            to_user=self.to_user
        )

        serialized_message = MessageSerializer(message_instance).data
        await self.channel_layer.group_send(
            self.conversation_name,
            {
                'type': 'send_message',
                'message': serialized_message
            }
        )

    async def send_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def get_receiver(self):
        usernames = self.conversation_name.split('__')
        for username in usernames:
            if username != self.from_user.username:
                return await sync_to_async(User.objects.get)(username=username)
