from django.urls import path
from . import views

urlpatterns = [
    path('activate/<slug:uidb64>/<slug:token>/', # email confirmation
        views.activate, name='activate'),
    path('<slug:username>/', views.profile, name='profile'), # profile
    path('<slug:username>/edit',views.edit, name='edit'), # profile edit
    path('follow/<slug:profile_pk>', views.follow, name='follow'), # user pressed follow button
    path('search/>', views.search, name='search_profile'),
]
