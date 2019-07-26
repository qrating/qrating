# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Question, Answer, Question_Image, Answer_Image
from .forms import QuestionForm, AnswerForm, Question_ImageForm, Answer_ImageForm,Question_ImageFormSet,Answer_ImageFormSet
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    questions = Question.objects.filter()
    return render(request, 'home.html',{'questions':questions})

@login_required
def create_question(request):
    #questions = Question.objects.filter()

    if request.method == 'POST':
        Question_form = QuestionForm(request.POST, request.FILES)
        image_formset = Question_ImageFormSet(request.POST, request.FILES)
        if Question_form.is_valid() and image_formset.is_valid():
            question = Question_form.save(commit = False)
            question.author = request.user
            question.time_created = timezone.now()
           
            # from django.db import transaction
            with transaction.atomic():
                question.save()
                image_formset.instance = question
                image_formset.save()
                return redirect('home')            
    else:
        Question_form = QuestionForm()
        image_formset = Question_ImageFormSet()

    return render(request, 'create_question.html',{'form':Question_form, 'image_formset':image_formset,})

def detail_question(request, pk):
    question = get_object_or_404(Question, pk=pk)    
    answers = Answer.objects.filter(question = pk)

    if request.method == "POST":
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.time_created = timezone.now()
            answer.save()
            return redirect('detail_question', pk=pk)
            
    elif request.method == "GET":
        form = AnswerForm()
        return render(request, "detail_question.html", {'question' : question, 'form' : form, 'answers' : answers})

def question_remove(request, pk):
    question=get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect('home')
