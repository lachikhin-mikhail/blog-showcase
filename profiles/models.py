from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from stdimage.models import StdImageField

    
class Profile(models.Model):
    """Fields that can be used for filling the profile page"""
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=160)
    profilePicture = StdImageField(upload_to='profileImages/')
    
    """Technical fields unaccessable for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    likes = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name='posts_liked')
    posts = models.ManyToManyField("posts.Post", related_name='posts_made')
    following = models.ForeignKey(User, on_delete=models.CASCADE)
    # favTags = models.ForeignKey("app.Model", on_delete=models.CASCADE) # to be implemented later
