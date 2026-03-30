import json
import re
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Post, Comment, Hashtag, Like, Profile, PostMedia
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages as flash_messages

def index(request):
    return render(request, 'main/index.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
        
def login(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = None

        if '@' in u:
            try:
                user_obj = User.objects.get(email=u)
                user = authenticate(request, username=user_obj.username, password=p)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(request, username=u, password=p)
            
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            flash_messages.error(request, 'Invalid username or password.', extra_tags='login_msg')
            
    return render(request, 'main/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        
        if not u or not e or not p:
            flash_messages.error(request, 'Please fill in all fields.', extra_tags='register_msg')
            return redirect('register')
            
        if User.objects.filter(username=u).exists():
            flash_messages.error(request, 'Username already exists.', extra_tags='register_msg')
            return redirect('register')
            
        if User.objects.filter(email=e).exists():
            flash_messages.error(request, 'Email already exists.', extra_tags='register_msg')
            return redirect('register')
            
        user = User.objects.create_user(username=u, email=e, password=p)
        auth_login(request, user)
        return redirect('index')
        
    return render(request, 'main/register.html')

def logout_user(request):
    auth_logout(request)
    return redirect('index')

def profile(request):
    return render(request, 'main/profile.html')

def notifications(request):
    return render(request, 'main/notifications.html')

def messages(request):
    return render(request, 'main/messages.html')

# --- JSON HELPER FUNCTIONS ---

def serialize_post(post, current_user=None):
    author = post.author
    likes_count = post.likes.count()
    comments_count = post.comments.count()
    user_liked = post.likes.filter(user=current_user).exists() if current_user and current_user.is_authenticated else False
    
    media = [{'url': m.file.url, 'type': m.type} for m in post.media.all()]
    
    has_profile = hasattr(author, 'profile')
    avatar_url = author.profile.avatar.url if has_profile and author.profile.avatar else '/static/main/assets/default.svg'
    display_name = author.profile.display_name if has_profile and author.profile.display_name else author.username
    
    res = {
        'id': post.id,
        'author': {
            'username': author.username,
            'display_name': display_name,
            'avatar': avatar_url,
        },
        'content': post.content,
        'created_at': post.created_at.isoformat(),
        'is_edited': post.is_edited,
        'media': media,
        'likes_count': likes_count,
        'comments_count': comments_count,
        'user_liked': user_liked,
    }
    
    if post.original_post:
        res['original_post'] = serialize_post(post.original_post, current_user)
        
    return res

def serialize_comment(comment, current_user=None):
    author = comment.author
    has_profile = hasattr(author, 'profile')
    avatar_url = author.profile.avatar.url if has_profile and author.profile.avatar else '/static/main/assets/default.svg'
    display_name = author.profile.display_name if has_profile and author.profile.display_name else author.username
    
    likes_count = comment.likes.count()
    user_liked = comment.likes.filter(user=current_user).exists() if current_user and current_user.is_authenticated else False
    
    return {
        'id': comment.id,
        'author': {
            'username': author.username,
            'display_name': display_name,
            'avatar': avatar_url,
        },
        'content': comment.content,
        'created_at': comment.created_at.isoformat(),
        'is_edited': comment.is_edited,
        'likes_count': likes_count,
        'user_liked': user_liked,
    }

def extract_hashtags_and_save(post):
    hashtags = re.findall(r'#(\w+)', post.content)
    hashtag_objs = []
    for tag in hashtags:
        obj, _ = Hashtag.objects.get_or_create(name=tag.lower())
        hashtag_objs.append(obj)
    post.hashtags.set(hashtag_objs)

# --- API ENDPOINTS ---

def api_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')
        
        search = request.GET.get('search', '')
        if search:
            posts = posts.filter(content__icontains=search)
            
        hashtag = request.GET.get('hashtag', '')
        if hashtag:
            posts = posts.filter(hashtags__name=hashtag.lower())
            
        return JsonResponse({'posts': [serialize_post(p, request.user) for p in posts]})
        
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
            
        content = request.POST.get('content', '')
        original_post_id = request.POST.get('original_post_id', None)
        
        original_post = None
        if original_post_id:
            try:
                original_post = Post.objects.get(id=original_post_id)
            except Post.DoesNotExist:
                pass

        if not content and not request.FILES and not original_post:
            return JsonResponse({'error': 'Post cannot be empty'}, status=400)

        post = Post.objects.create(
            author=request.user,
            content=content,
            original_post=original_post
        )
        
        for f in request.FILES.getlist('images'):
            PostMedia.objects.create(post=post, file=f, type=PostMedia.IMAGE)
        for f in request.FILES.getlist('videos'):
            PostMedia.objects.create(post=post, file=f, type=PostMedia.VIDEO)
            
        extract_hashtags_and_save(post)
        
        return JsonResponse({'post': serialize_post(post, request.user)})

def api_post_detail(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if not action and request.body:
             try:
                data = json.loads(request.body)
                action = data.get('action')
             except json.JSONDecodeError:
                pass
                
        if action == 'delete':
            if post.author != request.user:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
            post.delete()
            return JsonResponse({'success': True})
        elif action == 'edit':
            if post.author != request.user:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
                
            content = request.POST.get('content')
            if not content and request.body:
                try:
                    data = json.loads(request.body)
                    content = data.get('content')
                except json.JSONDecodeError:
                    pass

            if content is not None:
                post.content = content
                post.is_edited = True
                post.save()
                extract_hashtags_and_save(post)
            return JsonResponse({'post': serialize_post(post, request.user)})
            
    return JsonResponse({'error': 'Bad request'}, status=400)

def api_like_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)
            
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})

def api_comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
        
    if request.method == 'GET':
        comments = post.comments.all().order_by('created_at')
        return JsonResponse({'comments': [serialize_comment(c, request.user) for c in comments]})
        
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
            
        content = request.POST.get('content')
        if not content and request.body:
            try:
                data = json.loads(request.body)
                content = data.get('content')
            except json.JSONDecodeError:
                pass
                
        if not content:
            return JsonResponse({'error': 'Content required'}, status=400)
            
        comment = Comment.objects.create(
            author=request.user,
            post=post,
            content=content
        )
        return JsonResponse({'comment': serialize_comment(comment, request.user)})

def api_comment_detail(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if not action and request.body:
             try:
                data = json.loads(request.body)
                action = data.get('action')
             except json.JSONDecodeError:
                pass

        if action == 'delete':
            if comment.author != request.user:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
            comment.delete()
            return JsonResponse({'success': True})
        elif action == 'edit':
            if comment.author != request.user:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
                
            content = request.POST.get('content')
            if not content and request.body:
                try:
                    data = json.loads(request.body)
                    content = data.get('content')
                except json.JSONDecodeError:
                    pass

            if content is not None:
                comment.content = content
                comment.is_edited = True
                comment.save()
            return JsonResponse({'comment': serialize_comment(comment, request.user)})
            
    return JsonResponse({'error': 'Bad request'}, status=400)

def api_like_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method == 'POST':
        from .models import CommentLike
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)
            
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': comment.likes.count()})

def api_trending(request):
    if request.method == 'GET':
        trending = Hashtag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
        return JsonResponse({'trending': [{'name': t.name, 'count': t.post_count} for t in trending]})

def api_suggestions(request):
    if request.method == 'GET':
        users = User.objects.filter(posts__isnull=False).distinct()
        if request.user.is_authenticated:
            users = users.exclude(id=request.user.id)
        users = users.order_by('?')[:5]
        return JsonResponse({
            'suggestions': [{
                'id': u.id,
                'username': u.username,
                'display_name': u.profile.display_name if hasattr(u, 'profile') and u.profile.display_name else u.username,
                'avatar': u.profile.avatar.url if hasattr(u, 'profile') and u.profile.avatar else '/static/main/assets/default.svg'
            } for u in users]
        })
