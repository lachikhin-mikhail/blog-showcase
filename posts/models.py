from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Post(models.Model):
    caption = models.CharField(max_length=360)
    body = models.TextField()
    image = models.ImageField(null=True, blank=True)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        str=self.author.username
        str= self.date.strftime("%d/%m %H:%M ") + str + "'s post"
        return str
        
   
    
class Comments(models.Model):
    comment = models.TextField(max_length=2200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)

    def __str__(self):
        str=self.author.username
        str= str + "'s comment for " + self.parent_post.str()
        return str