from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from profiles.tokens import account_activation_token
from profiles.models import Profile

class LoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()


    def test_login(self):
        login_successful = self.client.login(
                                            username='testuser',
                                            password="12345"
                                            )
        self.assertTrue(login_successful)
        response = self.client.post(
                                    reverse('login'), 
                                    {'username':'testuser',
                                    'password':'12345'}
                                    )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # Test signing up and sending confirmation email
    def test_signing(self):
        response = self.client.post(
                        reverse('signup'),
                        {'username':'testuser2',
                        'email':'test@test.com',
                        'password1':'12fea345!',
                        'password2':'12fea345!'}
                        )
        user = User.objects.get(
                        username = 'testuser2',
                        is_active = False, # We need to ensure user is not active 
                        )                  # before they confirm email
        self.assertIsNotNone(mail.outbox)
        self.assertIsNotNone(user)

        # Test activation token worked and user is now active, profile created
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        self.client.post(
                        reverse('activate', kwargs={'uidb64':uid, 'token':token})
        )
        user = User.objects.get(
                                username="testuser2",
                                is_active = True
        )

        profile = Profile.objects.get(owner=user)
        self.assertIsNotNone(user)
        self.assertIsNotNone(profile)


