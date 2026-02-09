from . import views
from django.urls import path

app_name = 'account'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('signup/', views.signup, name='signup'),
]