from django.test import TestCase
from django.contrib.auth.models import User
from profiles.views import Profile
from posts.views import Post, Comments
from django.urls import reverse
import codecs
from django.db import connection


class PostDetalTesting(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='testuser')
        user1.set_password('test1')
        user1.save()
        Profile.objects.create(owner=user1)
        post = Post.objects.create(title="title", body='body', author=user1)
        Comments.objects.create(parent_post=post,
                                author=user1,
                                comment='comment')
        Comments.objects.create(parent_post=post,
                                author=user1,
                                comment='comment2')

    def test_post_loaded(self):
        post = Post.objects.get(title="title", body='body')
        response = self.client.get(
                reverse('post', kwargs={'post_pk': post.pk})
                )
        response_str = codecs.decode(response.content, 'UTF-8')
        self.assertIn(post.title, response_str)

    def test_comments_loaded(self):
        post = Post.objects.get(title="title", body='body')
        response = self.client.get(
                reverse('post', kwargs={'post_pk': post.pk})
                )
        response_str = codecs.decode(response.content, 'UTF-8')
        comment_count = response_str.count('comment-card')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts_comments\
                        WHERE posts_comments.parent_post_id = %s", [post.pk])
        comments_query = cursor.fetchall()
        comments_query_count = len(comments_query)
        self.assertEqual(comments_query_count, comment_count)
