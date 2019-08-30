# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill

PRICE = [(i*500+500,i*500+500) for i in range(10)]
DICT_PRICE = dict(PRICE)

CATEGORY_CHOICES = (
    ('economy','경제학'),
    ('programming', '프로그래밍'),
    ('math','수학'),
    ('management','경영학'),
    ('cpa','CPA/고시'),
    ('etc','기타'),
)

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length = 40)
    content = models.TextField()
    time_created = models.DateTimeField()
    price = models.IntegerField(choices=PRICE)
    selected = models.BooleanField(default=False)

    tags = models.ManyToManyField('Tag', blank  = True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='economy')

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    content = models.TextField()
    time_created = models.DateTimeField()
    selected = models.BooleanField(default=False)

class QuestionImage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AnswerImage(models.Model):
    answer = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length = 100)
    num = models.IntegerField(default=0)