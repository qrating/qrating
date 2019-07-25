from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate, logout as auth_logout
from django.http import HttpResponse

from .forms import UserRegsiterForm, ProfileRegsiterForm, LoginForm
from .models import Profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegsiterForm(data = request.POST)
        profile_form = ProfileRegsiterForm(data = request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()

            return redirect('home')
        
    else :
        user_form = UserRegsiterForm()
        profile_form = ProfileRegsiterForm()
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth_authenticate(username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')