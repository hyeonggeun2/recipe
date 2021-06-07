from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from members.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'members/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        user = User.objects.create_user(username=username, password=password, name=name)
        login(request, user)
        return redirect('index')

    return render(request, 'members/signup.html')


def logout_view(request):
    logout(request)
    return redirect('index')
