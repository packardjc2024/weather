from functools import wraps
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required


def conditional_login_required(view_func):
    """
    Only uses djangos built-in @login_required decorator if USE_ACCOUNT is True
    in the .env file. 
    """
    if not settings.USE_ACCOUNT:
        return view_func
    
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return login_required(view_func)(request, *args, **kwargs)
    return _wrapped_view


def otp_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:user_login')
        if not request.session.get('otp_verified'):
            return redirect('account:otp')
        return view_func(request, *args, **kwargs)
    return wrapper