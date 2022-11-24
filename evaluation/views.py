from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import User, Evaluations


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
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
            user = User.objects.create_user(request.POST['email'], request.POST['password'],
                                            first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                            phone_num=request.POST['phone_num'])
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
    if request.method == 'POST':
        form = RequestEvaluationForm(request.POST, request.FILES)
        if form.is_valid():  # figure out why this returns false
            evaluation = Evaluations(details=request.POST['details'], image=request.FILES['image'],
                                     contact_method=request.POST['contact_method'], user_id=request.user)
            evaluation.save()
            return render(request, 'evaluation/request_evaluation.html', {'request_submitted': True, 'form': form})
        else:
            return render(request, 'evaluation/request_evaluation.html', {'failed_request': True, 'form': form})
    else:
        form = RequestEvaluationForm()
    return render(request, 'evaluation/request_evaluation.html', {'form': form})


@login_required(login_url='/evaluation/')
def evaluations(request):
    return render(request, 'evaluation/evaluations.html')
