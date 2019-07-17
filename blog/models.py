# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

PRICE = [(i,i*500+500) for i in range(10)]

class Question(models.Model):
    title = models.CharField(max_length = 40)
    author = models.TextField(default='unknown')
    content = models.TextField()
    time_created = models.DateTimeField()
    price = models.IntegerField(choices=PRICE)
