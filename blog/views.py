# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import Question, Answer, QuestionImage, AnswerImage, DICT_PRICE, Tag
from .forms import QuestionForm, AnswerForm, TagForm
from accounts.models import Profile

def home(request):
    questions = Question.objects.filter()
    profiles = [question.author.profile for question in questions]

    tags = Tag.objects.order_by('num')
    print(tags)
    return render(request, 'home.html', {
        'question_profiles': zip(questions, profiles),
        'tags' : tags
        })

def create_question(request):
    if request.user.is_active == False:
        #return HttpResponse('로그인 또는 회원가입 후에 질문해 주세요.')
        return render(request, 'create_question.html')
    
    profile = get_object_or_404(Profile, user = request.user)
    coin = profile.coin
    

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        tag_form = TagForm(request.POST)
        price = DICT_PRICE.get(int(question_form['price'].value()))

        if question_form.is_valid() and profile.coin >= price:
            profile.coin -= price
            profile.save()

            question = question_form.save(commit = False)
            question.author = request.user
            question.time_created = timezone.now()

            # from django.db import transaction
            with transaction.atomic():
                question.save()

                if tag_form.is_valid():
                    for tag_name in tag_form['string'].value().replace(',', ' ').split():
                        
                        try:
                            tag = Tag.objects.get(name = tag_name)
                        except Tag.DoesNotExist:
                            tag = Tag(name = tag_name, num = 0)
    
                        tag.num += 1
                        tag.save()
                        question.tags.add(tag)

                for img in request.FILES.getlist('images'):
                    print(img)
                    instance = QuestionImage(
                        question=question,
                        image = img
                    )
                    print(instance)
                    instance.save()

                return redirect('home')
        else:
            return HttpResponse('질문 실패. 다시 시도해 보세요.')

    else:
        question_form = QuestionForm()
        tag_form = TagForm()

    
    return render(request, 'create_question.html',
        {
        'form':question_form,
        'coin':coin,
        'tag_form' : tag_form,
    })

#@login_required
def detail_question(request, pk):
    question = get_object_or_404(Question, pk=pk)    
    answers = Answer.objects.filter(question = pk)
    images = QuestionImage.objects.filter(question = pk)

    question_profile = get_object_or_404(Profile, user = question.author)
    answers_profile = [get_object_or_404(Profile, user = answer.author) for answer in answers]

    if request.method == "POST":
        answer_form = AnswerForm(request.POST)

        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.time_created = timezone.now()
            answer.save()
            return redirect('detail_question', pk=pk)
            
    elif request.method == "GET":
        answer_form = AnswerForm()

        return render(request, "detail_question.html", 
            {
                'question' : question,
                'images' : images,
                'form' : answer_form,
                'question_profile' : question_profile,
                'answers_profile':zip(answers, answers_profile),
        })

def question_remove(request, pk):
    question=get_object_or_404(Question, pk=pk)
    
    if request.user != question.author: #and not request.user.is_staff
        #messages.warning(request, '권한 없음')
        #return redirect('detail_question', pk=pk)
        return HttpResponse('권한 없음')
    else :
        for tag in question.tags.all():
            if tag.num == 1:
                tag.delete()
            else:
                tag.num -= 1

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

def answer_remove(request, qpk,apk):
    answer = get_object_or_404(Answer, pk=apk)
    question = get_object_or_404(Question, pk=qpk)
    answer.delete()
    return redirect('detail_question',pk=qpk)
    
def answer_update(request, qpk, apk):
    answer = get_object_or_404(Answer, pk=apk)
    question = get_object_or_404(Question, pk=qpk)
    
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('detail_question', pk=qpk)
    else:
        form = AnswerForm(instance = answer)
    return render(request, 'detail_question.html',{'form':form})

def cate_search(request, category):
    questions = Question.objects.filter()
    
    if category == 'all' :
        questions == Question.objects.all()
    elif category == 'economy' :
        questions = Question.objects.filter(category=category)
    elif category == 'programming' :
        questions = Question.objects.filter(category=category)
    elif category == 'math' :
        questions = Question.objects.filter(category=category)
    elif category == 'management' :
        questions = Question.objects.filter(category=category)
    elif category == 'cpa' :
        questions = Question.objects.filter(category=category)
    elif category == 'etc' :
        questions = Question.objects.filter(category=category)    
    return render(request, 'search.html', {'questions':questions})

def search(request):
    
    search_text = request.GET.get('search', None)
    tag = request.GET.get('tag', None)
    category = request.GET.get('cate', None)
    is_selected = request.GET.get('selected', None)

    if tag != None:
        questions = get_object_or_404(Tag, name = tag).question_set.all()
    else:
        questions = Question.objects.all()

    if search_text != None:
        questions = questions.filter(title__icontains = search_text)    

    if category != 'all' and category != None:
        questions = questions.filter(category=category)

    if is_selected != None:
        if is_selected == "T" :
            questions = questions.filter(selected = True)
        else :
            questions = questions.filter(selected = False)

    return render(request, 'search.html', {
        'questions' : questions
    })
