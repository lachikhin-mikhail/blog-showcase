from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile

class SearchTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="test1", password="test1")
        user2 = User.objects.create(username="test2", password="test2")
        user3 = User.objects.create(username="test3", password="test3")
        Profile.objects.create(owner=user1)
        Profile.objects.create(owner=user2)
        Profile.objects.create(owner=user3)

    def test_search(self):
        pass