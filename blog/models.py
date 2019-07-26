# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

#pip install django-imagekit / add setting.py apps 'imagekit'
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
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

def Question_path_image_path(instance, filename):
    return f"posts/{instance.post.content}/{filename}"

class Question_Image(models.Model):
    post = models.ForeignKey(Question, on_delete=models.CASCADE)
    file = ProcessedImageField(
        upload_to = 'images/',
        processors = [ResizeToFill(600,600)],
        format = 'JPEG',
        #option = {'quality':90},
    )

def Answer_path_image_path(instance, filename):
    return f'posts/{instance.post.content}/{filename}'

class Answer_Image(models.Model):
    post = models.ForeignKey(Answer, on_delete=models.CASCADE)
    file = ProcessedImageField(
        upload_to = 'images/',
        processors = [ResizeToFill(600,600)],
        format = 'JPEG',
        #option = {'quality':90},
    )