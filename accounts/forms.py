from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class UserRegsiterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'max_length':'15', 'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1' : forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2' : forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': '아이디',
            'email': '이메일',
            'password1': '패스워드',
            'password2': '패스워드 확인',
            
        }
    
class ProfileRegsiterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname']
        widgets ={
            'nickname': forms.TextInput(attrs={'class':'form-control', 'placeholder':'12자 이내로 입력 가능합니다'})
        }
        labels ={
            'nickname': '닉네임',
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
