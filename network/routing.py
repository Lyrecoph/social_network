from django.urls import path

from social import consumers
from tchat.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/notif/feed/", consumers.NotificationConsumer.as_asgi()),
    path("ws/tchat/room/<username>/", ChatConsumer.as_asgi()),

]