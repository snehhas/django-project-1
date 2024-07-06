# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after registration
            return redirect('home')  # Replace 'home' with your desired redirect URL
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})