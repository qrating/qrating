from django import forms
from .models import Question, Answer, QuestionImage, AnswerImage, PRICE

DICT_PRICE = dict(PRICE)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','content','price', ]

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', ]

class QuestionImageForm(forms.ModelForm):
    class Meta:
        model = QuestionImage
        fields = ['file',]

QuestionImageFormSet = forms.inlineformset_factory(Question, QuestionImage, form=QuestionImageForm, extra=3)

class AnswerImageForm(forms.ModelForm):
    class Meta:
        model = AnswerImage
        fields = ['file',]

AnswerImageFormSet = forms.inlineformset_factory(Answer, AnswerImage, form=AnswerImageForm, extra=3)