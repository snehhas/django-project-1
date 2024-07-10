from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if len(password2) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password2
