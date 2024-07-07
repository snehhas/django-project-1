# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Member
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')  # Assuming both passwords are the same due to validation

            user = form.save(commit=False)
            user.email = email
            user.save()

            # Create or link to Member model if needed
            # Example:
            # member = Member(user=user)
            # member.save()

            auth_login(request, user)  # Log the user in after registration
            return redirect('home')  # Replace 'home' with your desired redirect URL
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})
