from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate, logout as auth_logout
from django.http import HttpResponse

from .forms import UserRegsiterForm, ProfileRegsiterForm, LoginForm, CustomUserChangeForm
from .models import Profile
from blog.models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegsiterForm(data = request.POST)
        profile_form = ProfileRegsiterForm(data = request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            #user.is_active = False
            #주석을 해제할 경우, 회원가입 시 이메일 인증이 필요하다.
            #개발할때 불편할 것 같아 우선 주석처리함
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()

            auth_login(request, user)
            return redirect('send_email', user.pk)
        
    else :
        user_form = UserRegsiterForm()
        profile_form = ProfileRegsiterForm()
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def send_email(request, pk):
    user = get_object_or_404(User, pk = pk)

    message = render_to_string('activate_email.html',
    {
        'user': user,
        'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
        'token': account_activation_token.make_token(user),
    })
    
    mail_subject = "[SOT] 회원가입 인증 메일입니다."
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()

    return render(request, 'activating.html')
        
def activate(request, uid64, token):

    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return redirect('home')
    else:
        return HttpResponse('비정상적인 접근입니다.')

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
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('mypage',pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_pw.html', {
        'form': form
    })

def change_info(request,pk):
    user = User.objects.get(pk = pk)

    if request.method == "POST":
    	# 회원정보 변경 페이지에서
        user_change_form = CustomUserChangeForm(request.POST)
        new_nickname = user_change_form['nickname'].value()
        
        if user_change_form.is_valid():
            profile = get_object_or_404(Profile, user=user)
            profile.nickname = new_nickname
            profile.save()
            return redirect('mypage', pk)        
        else:
            return HttpResponse('잘못된 접근방식입니다.')        
    else:
        # 마이페이지에서 이동
        user_change_form = CustomUserChangeForm()

        return render(request, 'change_info.html',  {
            'user_change_form': user_change_form,
        })
