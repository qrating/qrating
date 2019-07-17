# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm
from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):
    questions = Question.objects.all
    return render(request, 'home.html',{'questions':questions})
    
def create_question(request):
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
            
    return render(request, 'create_question.html', {'form':form})