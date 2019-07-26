from django import forms
from .models import Question, Answer, Question_Image, Answer_Image

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','content','price', 'selected',]

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'selected',]

class Question_ImageForm(forms.ModelForm):
    class Meta:
        model = Question_Image
        fields = ['file',]

Question_ImageFormSet = forms.inlineformset_factory(Question, Question_Image, form=Question_ImageForm, extra=3)

class Answer_ImageForm(forms.ModelForm):
    class Meta:
        model = Answer_Image
        fields = ['file',]

Answer_ImageFormSet = forms.inlineformset_factory(Answer, Answer_Image, form=Answer_ImageForm, extra=3)