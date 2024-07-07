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

            # Create a new user object but do not save it yet
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # If you have additional fields in your Member model, you can create and link it here
            # Example:
            # member = Member(user=user)
            # member.save()

            auth_login(request, user)  # Log the user in after registration
            
            # Optionally, you may want to perform additional actions here, such as sending a welcome email

            return redirect('home')  # Redirect to the home page after successful registration
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})
