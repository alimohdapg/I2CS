from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import User


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'evaluation/index.html', {'failed_login': True, 'form': form})
    else:
        form = LoginForm()
    return render(request, 'evaluation/index.html', {'form': form})


@login_required(login_url='/evaluation/')
def home(request):
    return render(request, 'evaluation/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_num = request.POST['phone_num']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(email, password, first_name=first_name, last_name=last_name,
                                            phone_num=phone_num)
            user.save()
            login(request, user)
            return render(request, 'evaluation/home.html')
        else:
            return render(request, 'evaluation/signup.html', {'failed_signup': True, 'form': form})
    else:
        form = SignUpForm()
        return render(request, 'evaluation/signup.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required(login_url='/evaluation/')
def request_evaluation(request):
    return render(request, 'evaluation/home.html')