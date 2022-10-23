from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from posts.views import Post, Comments


class PostTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('test')
        user.save()
        Post.objects.create(title='title', body='body',author=user)
    def test_add_post(self):
        self.client.post(
                        reverse('login'), 
                        {'username':'testuser',
                        'password':'test'}
                        )
        # Post do not exist yet
        self.assertFalse(Post.objects.filter(title = 'title2'))
        self.client.post(
                    reverse('add_post'),
                    {'title':'title2',
                    'body':'body2'}
                    )
        # Post exists after request
        Post.objects.get(
                        title = 'title2'
                        )

    def test_add_comment(self):
        post = Post.objects.get(
                    title = 'title'
                    )
        comment=Comments.objects.filter(parent_post=post)
        self.assertFalse(comment)
        post_pk = post.pk

        self.client.post(
                reverse('login'), 
                {'username':'testuser',
                'password':'test'}
                )
        self.client.post(
                reverse('add_comment', kwargs={"post_pk":post_pk}), 
                {'body':'testcomment'}
                )
        Comments.objects.get(parent_post=post) 