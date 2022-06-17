from django.db import models
from stdimage.models import StdImageField
from django.conf import settings

class Post(models.Model):
    body = models.TextField()
    image = StdImageField(upload_to='postImages/')
    likes = models.IntegerField()
    reposts = models.IntegerField()
    is_reposted = models.BooleanField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    
class Comments(models.Model):
    comment = models.TextField(max_length=2200)
    commentator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent_post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)