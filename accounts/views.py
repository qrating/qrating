from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate, logout as auth_logout
from django.http import HttpResponse

from .forms import UserRegsiterForm, ProfileRegsiterForm, LoginForm
from .models import Profile
from blog.models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

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

            auth_login(request, user)
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

def mypage(request, pk):
    user = User.objects.get(pk = pk)
    print(request.user)
    print(user)
    if user == request.user:
        questions = Question.objects.filter(author = user)
        answers = Answer.objects.filter(author = user)
        profile = Profile.objects.get(user = user)

        return render(request, 'mypage.html', {
            'user':user, 
            'questions': questions,
            'answers' : answers,
            'profile' : profile,
            })
    else :
        return HttpResponse('본인이 아닙니다.')

def change_pw(request, pk):
    context= {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password,user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth_login(request,user)
                return redirect('home')
            else:
                context.update({'error':"새로운 비밀번호를 다시 확인해주세요."})
    else:
        context.update({'error':"현재 비밀번호가 일치하지 않습니다."})

    return render(request, 'change_pw.html',context)