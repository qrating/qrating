from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django.contrib.auth import password_validation

class UserRegsiterForm(UserCreationForm):
    
    password1 = forms.CharField(
        label="비밀번호",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={'maxlength':'15', 'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': '아이디',
            'email': '이메일',         
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
