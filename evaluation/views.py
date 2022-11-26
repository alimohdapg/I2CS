from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import User, Evaluations


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                logout(request)
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'evaluation/index.html', {'failed_login': True, 'form': form})
    else:
        form = LoginForm()
    return render(request, 'evaluation/index.html', {'form': form})


def home(request):
    return render(request, 'evaluation/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['password1'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'],
                                            phone_num=form.cleaned_data['phone_num'])
            logout(request)
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
            evaluation = form.save(commit=False)
            evaluation.user = request.user
            evaluation.save()
            return render(request, 'evaluation/request_evaluation.html', {'request_submitted': True, 'form': form})
        else:
            return render(request, 'evaluation/request_evaluation.html', {'failed_request': True, 'form': form})
    else:
        form = RequestEvaluationForm()
    return render(request, 'evaluation/request_evaluation.html', {'form': form})


@login_required(login_url='/evaluation/')
def evaluations(request):
    if request.user.is_staff == 0:
        return redirect('home')
    return render(request, 'evaluation/evaluations.html', {'evaluation_requests': Evaluations.objects.all()})
