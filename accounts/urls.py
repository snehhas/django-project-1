# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    # Add more URLs as needed
]
