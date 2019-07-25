# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PRICE = [(i,i*500+500) for i in range(10)]

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length = 40)
    content = models.TextField()
    time_created = models.DateTimeField()
    price = models.IntegerField(choices=PRICE)
    selected = models.BooleanField(default=False)
    image = models.ImageField(upload_to = 'images/', blank=True)

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    content = models.TextField()
    time_created = models.DateTimeField()
    selected = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/',blank=True)

