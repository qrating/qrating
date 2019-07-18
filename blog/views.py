# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):
    questions = Question.objects.filter(selected = True)

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit = False)
            question.author = request.user
            question.time_created = timezone.now()
            question.save()
            return redirect('home')
            
    else:
        form = QuestionForm()

    return render(request, 'home.html',{'questions':questions, 'form':form})

def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    
    answers = Answer.objects.filter(question = pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.time_created = timezone.now()
            answer.save()
            return redirect('question', pk=pk)
    elif request.method == "GET":
        form = AnswerForm()
        return render(request, "detail_question.html", {'question' : question, 'form' : form, 'answers' : answers})
            