from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    re_path(r'^signup/$', views.signup, name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/',
        views.activate, name='activate'),
    path('<slug:username>/', views.profile, name='profile'),
    path('<slug:username>/edit',views.edit, name='edit')
]
