from django.urls import path
from social import views

urlpatterns = [
    path('create-post/', views.PostCreateUpdateView.as_view(), name='create_post'),
    # path('create-post/', views.create_post, name='create_post'),
    # path('<int:post_id>/edit/', views.update_post, name='update_post'),
    path('post/update/<int:post_id>/', views.PostCreateUpdateView.as_view(), name='update_post'),
    # path('comment/add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/add/<int:post_id>/', views.CommentCreateUpdateView.as_view(), name='add_comment'),
    path('comment/update/<int:post_id>/<int:comment_id>/', views.CommentCreateUpdateView.as_view(), name='update_comment'),
    
    path('', views.post_list, name='post_list'),
    path('ajax-like/', views.like_item, name='like_item'),
    path('ajax-add-comment/', views.add_ajax_comment, name='add_ajax_comment'),

]
