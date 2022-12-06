from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .email_verification_token_generator import email_verification_token
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
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            body = render_to_string(
                'registration/email_verification.html',
                {
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': email_verification_token.make_token(user),
                }
            )
            EmailMessage(to=[user.email], subject=subject, body=body).send()
            return render(request, 'evaluation/signup.html', {'verify_email': True, 'email': user.email, 'form': form})
        else:
            return render(request, 'evaluation/signup.html', {'failed_signup': True, 'form': form})
    else:
        form = SignUpForm()
    return render(request, 'evaluation/signup.html', {'form': form})


def get_user_from_email_verification_token(uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError,
            User.DoesNotExist):
        return None
    if user is not None \
            and \
            email_verification_token.check_token(user, token):
        return user
    return None


def activate_user(request, uidb64, token):
    user = get_user_from_email_verification_token(uidb64, token)
    user.is_active = True
    user.save()
    logout(request)
    login(request, user)
    return redirect('home')


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
