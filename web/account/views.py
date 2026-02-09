from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from .models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .functions import *
from .forms import SignUpForm


def index(request):
    """
    Main account page. User can login or sign up here.
    """
    context = {}
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, 'account/index.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return redirect(settings.LOGIN_URL)


def user_logout(request):
    """
    """
    logout(request)
    request.session.flush()
    return redirect(settings.LOGOUT_REDIRECT_URL)


def signup(request):
    """
    """
    context = {}
    # USE_EMAIL in settings.py is conditional accoutn for here 
    # if request.method == 'GET':
    #     return render(request, 'account/signup.html', context)
    # elif request.method == 'POST':
    #     first_name = request.POST.get('first_name')
    #     last_name = request.POST.get('last_name')
    #     email = request.POST.get('email_name')
    #     body = (
    #         'Your Signup Link,\n\n'
    #         'Your signup code is:\n\n'
    #         f'111222333\n\n'
    #         f'This code expires at \n\n'
    #         'Packard Social Media Admin'
    #     )
    #     send_mail(
    #         'Packard Social Media Admin', 
    #         body,
    #         settings.DEFAULT_FROM_EMAIL, 
    #         [email]
    #     )
        # return redirect('account:index')
    return redirect('account:index')



