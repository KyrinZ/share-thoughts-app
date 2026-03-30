from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def login(request):
    return render(request, 'main/login.html')

def register(request):
    return render(request, 'main/register.html')

def profile(request):
    return render(request, 'main/profile.html')

def notifications(request):
    return render(request, 'main/notifications.html')

def messages(request):
    return render(request, 'main/messages.html')
