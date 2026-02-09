from django.urls import path
from . import views
from account.decorators import conditional_login_required


app_name = 'docs'

urlpatterns = [
    path('', conditional_login_required(views.index), name='index'),
]