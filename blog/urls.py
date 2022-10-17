
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import start


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start),
    path('posts/', include('posts.urls')),
    path('profile/', include('profiles.urls')),
    path('posts/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
