# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import Question, Answer, QuestionImage, AnswerImage, DICT_PRICE
from .forms import QuestionForm, AnswerForm, QuestionImageForm, AnswerImageForm, QuestionImageFormSet,AnswerImageFormSet
from accounts.models import Profile

def home(request):
    questions = Question.objects.filter()
    return render(request, 'home.html',{'questions':questions})

@login_required
def create_question(request):
    profile = get_object_or_404(Profile, user = request.user)
    coin = profile.coin

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        image_formset = QuestionImageFormSet(request.POST, request.FILES)
        price = DICT_PRICE.get(int(question_form['price'].value()))

        if question_form.is_valid() and image_formset.is_valid() and profile.coin >= price:
            profile.coin -= price
            profile.save()

            question = question_form.save(commit = False)
            question.author = request.user
            question.time_created = timezone.now()
           
            # from django.db import transaction
            with transaction.atomic():
                question.save()
                image_formset.instance = question
                image_formset.save()
                return redirect('home')
        else:
            return HttpResponse('질문 실패. 다시 시도해 보세요.')

    else:
        question_form = QuestionForm()
        image_formset = QuestionImageFormSet()

    
    return render(request, 'create_question.html',
        {
        'form':question_form, 
        'image_formset':image_formset,
        'coin':coin,
    })

@login_required
def detail_question(request, pk):
    question = get_object_or_404(Question, pk=pk)    
    answers = Answer.objects.filter(question = pk)

    


    if request.method == "POST":
        answer_form = AnswerForm(request.POST)#, request.FILES)
        image_formset = AnswerImageFormSet(request.POST, request.FILES)

        if answer_form.is_valid() and image_formset.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.time_created = timezone.now()
            answer.save()
            return redirect('detail_question', pk=pk)
            
    elif request.method == "GET":
        answer_form = AnswerForm()
        image_formset = AnswerImageFormSet()
        return render(request, "detail_question.html", 
            {'question' : question, 
            'form' : answer_form, 
            'answers' : answers, 
            'image_formset':image_formset,
        })

def question_remove(request, pk):
    question=get_object_or_404(Question, pk=pk)
    
    if request.user != question.author: #and not request.user.is_staff
        #messages.warning(request, '권한 없음')
        #return redirect('detail_question', pk=pk)
        return HttpResponse('권한 없음')
    else :
        question.delete()
        return redirect('home')

def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk)
    profile = get_object_or_404(Profile, user = request.user)
    coin = profile.coin

    if request.user != question.author:
        #messages.warning(request, "권한 없음")#외않작동?
        #return redirect('detail_question', pk=pk)
        return HttpResponse('권한 없음')
    
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)        
        price_new = DICT_PRICE.get(int(form['price'].value()))
        price_old = DICT_PRICE.get(question.price)

        if form.is_valid() and coin >= price_new - price_old:
            profile.coin -= price_new - price_old
            profile.save()

            question.title = form['title'].value()
            question.content = form['content'].value()
            question.price = form['price'].value()
            question.save()
            
            return redirect('detail_question', pk=pk)
    else:
        form = QuestionForm(instance=question)
    return render(request,'update_question.html',{'form':form})

def select_question(request, qpk, apk):
    question = get_object_or_404(Question, pk=qpk)    
    answer = get_object_or_404(Answer, pk=apk)
    profile_answer = get_object_or_404(Profile, user=answer.author)

    if request.user != question.author or question.selected :
        return HttpResponse('잘못된 요청입니다.')
    else :
        question.selected = True
        answer.selected = True
        profile_answer.coin += DICT_PRICE[question.price]
        question.save()
        answer.save()
        profile_answer.save()

        return redirect('detail_question', pk=qpk)


"""
def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.user != question.author:
        #messages.warning(request, '권한 없음') 이것저것 설치해야함
        return redirect('detail_question')
    if request.method == "POST":
        form = QuestionForm(request.POST, instance = question)
        if form.is_vaild():
            form.save()
            return redirect(question)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'detail_question.html', {'form':form})


def answer_remove(request, pk):
    answer=get_object_or_404(Answer, pk=pk)
    answer.delete()
    return redirect('detail_question')
"""
