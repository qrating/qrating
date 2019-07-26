from django import forms
from .models import Question, Answer, QuestionImage, AnswerImage

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','content','price', 'selected',]

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'selected',]

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