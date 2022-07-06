from django.db import models
from stdimage.models import StdImageField
from django.conf import settings
from django.contrib.auth.models import User


class Post(models.Model):
    body = models.TextField()
    image = StdImageField(upload_to='postImages/')
    likes = models.IntegerField()
    reposts = models.IntegerField()
    is_reposted = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    
    
class Comments(models.Model):
    comment = models.TextField(max_length=2200)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)