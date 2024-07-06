# accounts/models.py
from django.contrib.auth.models import User
from django.db import models

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add more fields as needed
