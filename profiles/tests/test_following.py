from django.test import TestCase
from profiles.models import Profile, Following
from django.contrib.auth.models import User
from django.urls import reverse


class ProfileEditTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('test')
        user.save()
        user2 = User.objects.create(username='testuser2')
        user2.set_password('test')
        user2.save()       
        Profile.objects.create(owner=user, name='test1')
        Profile.objects.create(owner=user2, name='test2')

    def test_following(self):
        # Login current user
        self.client.post(
                reverse('login'), 
                {'username':'testuser',
                'password':'test'}
                )
        # Getting profiles and sending request
        profile1 = Profile.objects.get(name='test1')
        profile2 = Profile.objects.get(name='test2')
        self.client.post(
                        reverse('follow', kwargs={'profile_pk':profile2.pk}),
                            )
        Following.objects.get(profile=profile2, following_user=profile1)