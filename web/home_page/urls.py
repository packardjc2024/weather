from django.urls import path
from . import views
from account.decorators import conditional_login_required


app_name = 'home_page'

urlpatterns = [
    path('', conditional_login_required(views.index), name='index'),
    path('search/', conditional_login_required(views.search), name='search'),
    path('delete_location/', conditional_login_required(views.delete_location), name='delete_location'),
]