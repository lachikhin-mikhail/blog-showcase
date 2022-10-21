from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments
from profiles.models import Profile, Following
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def home(request, followed_feed=False):
    # Posts from followed authors
    if followed_feed is True:
        if request.user.is_authenticated:
            current_user = request.user
            current_profile = Profile.objects.get(owner=current_user)
            followed_obj = Following.objects.filter(
                        following_user=current_profile
                        )
            followed_author_list = []
            for followed in followed_obj:
                followed_author_list.append(followed.profile.owner)
            posts = Post.objects.none()
            for author in followed_author_list:
                posts |= Post.objects.filter(author=author)
            posts = posts.order_by('date').reverse()
            return render(request, 'main.html', {'posts': posts})
        else:
            posts = Post.objects.all().order_by('date').reverse()
            return render(request, 'main.html', {'posts': posts})
    # Search query  
    elif request.method == 'POST':
        search = request.POST['search']
        posts = Post.objects.filter(title__contains=search)
        if posts:
            return render(request, 'main.html', {'posts': posts})
        else:
            return redirect('error', 'post_not_found')
    # All posts
    else:
        posts = Post.objects.all().order_by('date').reverse()
        return render(request, 'main.html', {'posts': posts})


def post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    try:
        comments = Comments.objects.filter(parent_post=post) \
            .order_by('date').reverse()
        return render(request, 'post.html', {
            'post': post,
            'comments': comments
            })
    except ValueError:
        return redirect('error', 'post_not_found')
    


@login_required(login_url=reverse_lazy('signup'))
def add(request):
    if request.method == "POST":
        try:
            Post.objects.create(title=request.POST['title'],
                                body=request.POST['body'],
                                image=request.FILES['image'],
                                author=request.user)
            return redirect('home')
        except:
            Post.objects.create(title=request.POST['title'],
                                body=request.POST['body'],
                                author=request.user)
            return redirect('home')
    else:
        return render(request, 'addPost.html')

@login_required(login_url=reverse_lazy('signup'))
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    try:
        if request.method == "POST":
            Comments.objects.create(comment=request.POST["body"],
                                    parent_post=post,
                                    author=request.user)
            return redirect('post', post_pk)
        else:
            return render(request, 'addComment.html', {'post_pk':post_pk})
    except ValueError:
        return redirect('error', 'post_not_found')


@login_required(login_url=reverse_lazy('signup'))
def like(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.likes.filter(pk=request.user.pk):
            post.likes.remove(request.user)
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            post.likes.add(request.user)
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
