from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from profiles.models import Profile, Following
from posts.models import Post
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db import ProgrammingError
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

""" def signup(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'signup.html', {'error': 'Passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'signup.html')
 """

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'Username has already been taken ☹️'})
            except User.DoesNotExist:
                if User.objects.filter(email=request.POST['email']).exists():
                    return render(request, "signup.html",{'error': "This email is already used 🤔"})
                else:
                    user = User.objects.create_user(request.POST['username'],
                                                    email=request.POST['email'],
                                                    password=request.POST['password1'])
                    user.is_active = False
                    user.save()
                    profile = Profile.objects.create(owner=user)

                    
                    #auth.login(request, user)
                    current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

            
        else:
            return render(request, 'signup.html', {'error': 'Passwords must match'})
    else:
        return render(request, 'signup.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!' + user)

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user=user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def profile(request, username):
    try:
        # profile owner
        user = User.objects.get(username=username)
        profile = Profile.objects.get(owner=user)
        posts = Post.objects.filter(author=user)
        # Numbers
        # postsNum = profile.postNum
        # followersNum = profile.followersNum
        # followingNum = profile.followingNum
        # User browsing
        current_user = User.objects.get(pk=request.user.pk)
        current_user_profile = Profile.objects.get(owner=current_user)
        # Check if current user already following this account
        already_following = Following.objects.filter(profile=profile, following_user=current_user_profile).exists()

        return render(request, 'profile.html', {'owner':user, 'profile':profile, \
             'posts':posts, "already_following":already_following })
    except User.DoesNotExist:
        return redirect('error', 'profile_not_found')

def edit(request, username):
    # Entering the page
    if not request.user.is_authenticated:
        return redirect('signup')
    try:
        user = User.objects.get(username=username)
        if user == request.user:
            profile = Profile.objects.get(owner=user)
            # Edit sumbitted
            if request.method == 'POST':    
                try:
                    profile.profilePicture = request.FILES['pfp']
                except:
                    pass
                profile.name = request.POST['name']
                profile.bio = request.POST['bio']
                
                profile.save()
                return redirect('profile', username=username) 
            else:
            # Edit entered
                return render(request, 'edit.html', {'owner':user , 'profile':profile })
        else:
            return render(request, 'profile.html', {'owner':user})
    except User.DoesNotExist:
        return redirect('error', 'profile_not_found')

@login_required(login_url=reverse_lazy('signup'))
def follow(request, profile_pk):
    if request.method == 'POST':
        current_user = get_object_or_404(Profile, owner=request.user)
        to_follow_profile = get_object_or_404(Profile, pk=profile_pk)
        if Following.objects.filter(profile=to_follow_profile, following_user=current_user).exists():
            try:
                follow=Following.objects.get(profile=to_follow_profile, following_user=current_user)
                follow.delete()
            except:
                pass
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            Following.objects.create(profile=to_follow_profile, following_user=current_user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def search(request):
    if request.method == 'POST':
        users = User.objects.filter(username__contains=request.POST['search'])
        profiles = Profile.objects.none()
        for user in users:
            profiles |= Profile.objects.filter(owner=user)
        if profiles:
            return render(request, 'search_profile.html', {'matching_profiles':profiles })
        else:
            return redirect('error', 'profile_not_found')
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))