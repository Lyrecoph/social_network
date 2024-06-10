import json

from channels.generic.websocket import  AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from social.serializers import NotificationSerializer
from social.models import Notification

# Cette classe permet d'envoyer les données depuis le serveur

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
      self.group_name = "notification"
      await  self.accept()
      await self.channel_layer.group_add(self.group_name, self.channel_name)
      await self.send(text_data=json.dumps({"message": "Hello proxi", "name": "greeting"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        
   
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event = {"type" : "send_notif"}
            
        if text_data_json['type'] == "notif_feed":
            data_json = await self.get_notif_from_db(type='notif_feed')
            event["message"] = data_json
            event["name"] = "notif_feed"


        if text_data_json['type'] == "notif_list":
            data_json = await self.get_notif_from_db()
            event["message"] = data_json
            event["name"] = "notif_list"

        if text_data_json['type']  == "notif_read":
            notif_id = text_data_json["message"]
            await self.mark_notif_as_read(notif_id)
            data_json = await self.get_notif_from_db(type='notif_feed')
            event["message"] = data_json
            event["name"] = "notif_feed"

        await self.channel_layer.group_send(self.group_name, event)
        return await super().receive(text_data)

    # envoie les données récupérer au niveau de la DB
    async def send_notif(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_notif_from_db(self, type=None):
        notif_list = Notification.objects.all()
        if type == "notif_feed":
            notif_list = notif_list[:10]
        serializer = NotificationSerializer(notif_list, many=True)
        return json.dumps(serializer.data)

    @database_sync_to_async
    def mark_notif_as_read(self, notif_id):
        try:
            notif = Notification.objects.get(id=notif_id)
            notif.read = True
            notif.save()
        except:
            pass