from django.urls import path

from social import consumers

websocket_urlpatterns = [
    path("ws/notif/feed/", consumers.NotificationConsumer.as_asgi()),
]