from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class UserRegsiterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1','password2']

class ProfileRegsiterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
