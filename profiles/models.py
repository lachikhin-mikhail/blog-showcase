from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from stdimage import StdImageField

    
class Profile(models.Model):
    """Fields that can be used to modify the profile page"""
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=160)
    profilePicture = StdImageField(upload_to='profileImages/')
    
    """Technical fields unaccessable for users"""
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    likes = models.ForeignKey("posts.Post", on_delete=models.SET_NULL, related_name='posts_liked',null=True, blank=True)
    
    # Here I want to make "posts" category, so user can also repost others posts
    # so pulling someone's posts by "author" field from "post" model wont be good enough
    posts = models.ForeignKey("posts.Post", on_delete=models.SET_NULL, related_name='posts_made',null=True, blank=True)
    following = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        str=self.owner.username
        str=str + "'s profile"
        return str
        
