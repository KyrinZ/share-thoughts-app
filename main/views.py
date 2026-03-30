from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages as flash_messages

def index(request):
    return render(request, 'main/index.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = None

        # If user passed email instead of username
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
            flash_messages.success(request, 'Logged in successfully.')
            return redirect('index')
        else:
            flash_messages.error(request, 'Invalid username or password.')
            
    return render(request, 'main/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        
        if not u or not e or not p:
            flash_messages.error(request, 'Please fill in all fields.')
            return redirect('register')
            
        if User.objects.filter(username=u).exists():
            flash_messages.error(request, 'Username already exists.')
            return redirect('register')
            
        if User.objects.filter(email=e).exists():
            flash_messages.error(request, 'Email already exists.')
            return redirect('register')
            
        user = User.objects.create_user(username=u, email=e, password=p)
        auth_login(request, user)
        flash_messages.success(request, 'Registration successful. Welcome!')
        return redirect('index')
        
    return render(request, 'main/register.html')

def logout_user(request):
    auth_logout(request)
    flash_messages.success(request, 'Logged out successfully.')
    return redirect('login')

def profile(request):
    return render(request, 'main/profile.html')

def notifications(request):
    return render(request, 'main/notifications.html')

def messages(request):
    return render(request, 'main/messages.html')
