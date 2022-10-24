from django.test import TestCase
from posts.models import Post
from django.contrib.auth.models import User
from django.urls import reverse


class LikesTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('test')
        user.save()
        Post.objects.create(title="post", body="text",author=user)
 

    def test_following(self):
        # Login current user
        self.client.post(
                reverse('login'), 
                {'username':'testuser',
                'password':'test'}
                )
        # Getting post
        post = Post.objects.get(title="post")
        # Asserting it has no likes
        self.assertEqual(post.likes.count(), 0)
        # Sending request
        self.client.post(
                        reverse('like', kwargs={'post_pk':post.pk}),
                            )
        # Asserting it now has a like
        self.assertEqual(post.likes.count(), 1)
