from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:post_id>/',views.post, name='post')
]
