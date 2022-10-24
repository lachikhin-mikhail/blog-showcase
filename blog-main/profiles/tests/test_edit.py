from django.test import TestCase
from profiles.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse


class ProfileEditTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('test')
        user.save()
                            
        Profile.objects.create(
                                owner=user,
                                name='test1',
                                bio='test1'
                                )
    def test_edit(self):
        # Getting profile owner
        user = User.objects.get(
                                username='testuser'
                                )
        # Checking profile exists with old data
        Profile.objects.get(
                            owner=user,
                            name='test1',
                            bio='test1'
                            )

        # Login user so we can edit his profile
        self.client.post(
                        reverse('login'), 
                        {'username':'testuser',
                        'password':'test'}
                        )
        # Changing profile
        self.client.post(
                        reverse('edit', kwargs={'username':user.username}),
                        {'name':'test2',
                        'bio':'test2'}
                        ) 
        # Checking profile with new data exists    
        Profile.objects.get(
                    owner=user,
                    name='test2',
                    bio='test2'
                    )