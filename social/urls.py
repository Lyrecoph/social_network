from django.urls import path
from social import views
urlpatterns = [
    path('create-post/', views.create_post, name='create_post'),
    path('', views.post_list, name='post_list'),
]
