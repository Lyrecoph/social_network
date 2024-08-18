
from django.urls import path
from . import views
urlpatterns = [
    path('<username>/', views.tchat_home, name="tchat_home"),
    path('messages/<str:conversation_name>/', views.get_conversation_messages, name='get_conversation_messages'),
]

