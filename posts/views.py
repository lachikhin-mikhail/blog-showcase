from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments
from profiles.models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def home(request):
    posts = Post.objects.all().order_by('date').reverse()
    return render(request, 'main.html', {'posts':posts })

def post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    try:
        comments= Comments.objects.filter(parent_post=post).order_by('date').reverse()
        return render(request, 'post.html', {'post':post, 'comments':comments})
    except ValueError:
        return HttpResponseNotFound('Post does not exist, something wrong here')
    


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
        return HttpResponseNotFound('Post does not exist, something wrong here')


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

