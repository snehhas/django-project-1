# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('user_list/', views.user_list, name='user_list'),
]
