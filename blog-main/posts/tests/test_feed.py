from django.test import TestCase
from django.contrib.auth.models import User
from profiles.views import Profile, Following
from posts.views import Post
from django.urls import reverse
import codecs
from django.db import connection

class SearchTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='testuser')
        user1.set_password('test1')
        user1.save()
        user2 = User.objects.create(username='testuser2')
        user2.set_password('test2')
        user2.save()
        profile1 = Profile.objects.create(owner=user1)
        profile2 = Profile.objects.create(owner=user2)
        Following.objects.create(profile=profile1, following_user=profile2)
        Post.objects.create(title="title", body='body', author=user1)
        Post.objects.create(title="title2", body='body2', author=user1)
        Post.objects.create(title="not", body='body3', author=user2)

    def test_home_feed(self):
        # Counting profiles returned by view
        response = self.client.get(
                reverse('home')
                )
        response_str = codecs.decode(response.content, 'UTF-8')
        profile_count = response_str.count('post-card')
        # Counting posts returned by direct query
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts_post")
        profile_query = cursor.fetchall()
        profile_query_count = len(profile_query)
        # Testing feed gives exact amount
        self.assertEqual(profile_query_count, profile_count)


    def test_following_feed(self):
                # Counting profiles returned by view
        self.client.post(
                        reverse('login'), 
                        {'username':'testuser2',
                        'password':'test2'}
                    )
        response = self.client.get(
                reverse('home', kwargs={'followed_feed':True})
                )
        response_str = codecs.decode(response.content, 'UTF-8')
        profile_count = response_str.count('post-card')
        # Testing feed gives exact amount
        self.assertEqual(profile_count, 2)


    def test_search_feed(self):
        # Counting profiles returned by view
        response = self.client.post(
                reverse('home'),
                {'search':'title',}
                )
        response_str = codecs.decode(response.content, 'UTF-8')
        profile_count = response_str.count('post-card')
        # Counting profiles returned by direct query
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts_post\
                        WHERE posts_post.title LIKE '%title%'")
        post_query = cursor.fetchall()
        post_query_count = len(post_query)
        # Testing search dont give us excessive data
        self.assertEqual(post_query_count, profile_count)

