from multiprocessing import context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from .forms import *
from .models import *
from .myfunctions import post_jsonify

# Number of post for pagination
NUMBER_OF_POSTS = 10

# Landing page view
def landing_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:home'))
    return render(request, 'main/landing_page.html')

def home(request):
    context = {}
    return render(request, 'home.html', context)
    
def profile(request):
    context = {}
    return render(request, 'profile.html', context)

def login(request):
    context = {}
    return render(request, 'login.html', context)

def registration(request):
    context = {}
    return render(request, 'registration.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)

def home2(request):
    post_form = PostForm()

    if request.method == 'POST':
        post = Post(user=request.user)
        post_form = PostForm(request.POST, instance=post)

        if post_form.is_valid():
            post_form.save()

            messages.success(request, 'You created a new post.')
            return HttpResponseRedirect(reverse('main:home'))

    posts = Post.objects.order_by('-date_posted')

    # This variable is for javascript
    total_paginated_pages = Paginator(posts, NUMBER_OF_POSTS).num_pages

    return render(request, 'main/home.html', {
        'total_paginated_pages': total_paginated_pages,
        'post_form': post_form,
        'posts': posts,
        'background': 'home-bkg-img'
    })


# Post View
@login_required(login_url='login_register:login')
def post(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post_id)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment = Comment(user=request.user, post=post)
        comment_form = CommentForm(request.POST, instance=comment)

        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, 'You commented')
            return HttpResponseRedirect(reverse('main:post', args=[post_id]))

    return render(request, 'main/post.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'background': 'post-bkg-img'
    })


# About View
@login_required(login_url='login_register:login')
def about2(request):
    return render(request, 'main/about.html', {
        'background': 'about-bkg-img'
    })


# Filter view to filter all the post
@login_required(login_url='login_register:login')
def filtering(request, filter_key):

    # The filter key is stored in session so 'Post Json view' can access it
    request.session['filter'] = filter_key
    return HttpResponseRedirect(reverse('main:home'))


# View for liking the post
@login_required(login_url='login_register:login')
def liking_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(id=request.user.id)

    # like object is created and if it exists liked value set to false
    liked = LikeForPost.objects.get_or_create(post=post, user=user)
    if not liked[1]:
        liked[0].liked = False
        liked[0].save()
    is_liked = liked[0].liked

    # All the like object that has attribute 'liked' set to false is deleted
    LikeForPost.objects.filter(liked=False).delete()
    # Json value
    item = {
        'total_like_post': LikeForPost.objects.filter(post=post).count(),
        'liked': is_liked
    }
    return HttpResponse(json.dumps(item))


# Similar to Post this view is for comments
@login_required(login_url='login_register:login')
def liking_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    user = User.objects.get(id=request.user.id)

    # Checks whether user liked the comment by querying the database.
    # If found 'liked' attribute is set to false

    liked = LikeForComment.objects.get_or_create(comment=comment, user=user)
    if not liked[1]:
        liked[0].liked = False
        liked[0].save()
    is_liked = liked[0].liked

    LikeForComment.objects.filter(liked=False).delete()
    # Json value
    item = {
        'total_like_comment': LikeForComment.objects.filter(comment=comment).count(),
        'liked': is_liked
    }
    return HttpResponse(json.dumps(item))


# ALL VIEWS BELOW IS FOR JSON API, SO JAVACRIPT CAN USE IT

# Post Json view
@login_required(login_url='login_register:login')
def post_json_format(request, pg):

    # Checks for filter key in session and if not found default is set to 'latest'
    try:
        filter_key = request.session['filter']
        request.session['filter'] = None
    except KeyError:
        filter_key = 'latest'

    post_list = Post.filtering_posts(filter_key)
    paginated_post_list = Paginator(post_list, NUMBER_OF_POSTS)

    # Paginated posts is turned to json format with help of custom function defined in myfunction
    json_posts = post_jsonify(
        paginated_post_list.get_page(pg))

    return HttpResponse(json_posts)


# Liked info for post in Json format
@login_required(login_url='login_register:login')
def like_post_json(request, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(id=request.user.id)
    try:
        liked = LikeForPost.objects.get(post=post, user=user)
        liked = liked.liked
    except ObjectDoesNotExist:
        liked = False

    # Json value
    item = {
        'total_like_post': LikeForPost.objects.filter(post=post).count(),
        'liked': liked
    }
    return HttpResponse(json.dumps(item))


# Liked info for comment in Json format
@login_required(login_url='login_register:login')
def like_comment_json(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    user = User.objects.get(id=request.user.id)
    try:
        liked = LikeForComment.objects.get(comment=comment, user=user)
        liked = liked.liked
    except ObjectDoesNotExist:
        liked = False

    # Json value
    item = {
        'total_like_comment': LikeForComment.objects.filter(comment=comment).count(),
        'liked': liked
    }
    return HttpResponse(json.dumps(item))
