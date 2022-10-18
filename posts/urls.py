from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:post_pk>/',views.post, name='post'),
    path('like/<int:post_pk>', views.like, name='like'),
    path('new/', views.add, name='add_post'),
    path('new/comment/<int:post_pk>', views.comment, name='add_comment')
]
