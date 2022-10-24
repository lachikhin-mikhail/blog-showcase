from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile
from django.urls import reverse
import codecs
from django.db import connection

class SearchTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="test1", password="test1")
        user2 = User.objects.create(username="test2", password="test2")
        user3 = User.objects.create(username="test3", password="test3")
        Profile.objects.create(owner=user1)
        Profile.objects.create(owner=user2)
        Profile.objects.create(owner=user3)

    def test_search(self):
        # Counting profiles returned by view
        response = self.client.post(
                reverse('search_profile'),
                {'search':'1',}
                )
        response_str = codecs.decode(response.content, 'UTF-8')
        profile_count = response_str.count('profile-found')
        # Counting profiles returned by direct query
        cursor = connection.cursor()
        cursor.execute("SELECT auth_user.username FROM auth_user\
                        INNER JOIN profiles_profile\
                        ON auth_user.id = profiles_profile.owner_id\
                        WHERE auth_user.username LIKE '%2%'")
        profile_query = cursor.fetchall()
        profile_query_count = len(profile_query)
        # Testing search dont give us excessive data
        self.assertEqual(profile_query_count, profile_count)

        