from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # home
    path('followed/<slug:followed_feed>/', views.home, name='home'), # show posts from followed authors
    path('<int:post_pk>/',views.post, name='post'), # post details
    path('like/<int:post_pk>', views.like, name='like'), # user pressed on like
    path('new/', views.add, name='add_post'), # user wants to add a post
    path('new/comment/<int:post_pk>', views.comment, name='add_comment') # user wants to add comment
]
