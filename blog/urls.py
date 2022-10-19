
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import start, error
from profiles import views


urlpatterns = [
    path('login', views.login, name='login'), # login
    path('logout', views.logout, name='logout'), # logout
    path('signup', views.signup, name='signup'), # signup
    path('admin/', admin.site.urls),
    path('', start), # Redirect to home page from posts
    path('error/<str:error>', error, name='error'),
    path('posts/', include('posts.urls')),
    path('profile/', include('profiles.urls')),
    path('posts/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
