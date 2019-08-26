from django import forms
from .models import Question, Answer, QuestionImage, AnswerImage, PRICE, Tag

DICT_PRICE = dict(PRICE)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','content','price',]
        widgets={
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'화이팅><'}),
            'price' : forms.Select(attrs={'class':'form-control'}),
        }
        labels={
            'title': '제목',
            'content': '내용',
            'price' : '코인'
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', ]
        widgets={
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'답변을 입력하세요'}),
        }
        labels={
            'content':'내용',
        }
class QuestionImageForm(forms.ModelForm):
    class Meta:
        model = QuestionImage
        fields = ['file',]
        widgets={
            'file':forms.FileInput(attrs={'class':'fileclass'}),
        }
        labels={
            'file': '이미지 파일',
        }

QuestionImageFormSet = forms.inlineformset_factory(Question, QuestionImage, form=QuestionImageForm, extra=3)

class AnswerImageForm(forms.ModelForm):
    class Meta:
        model = AnswerImage
        fields = ['file',]
        widgets={
            'file':forms.FileInput(attrs={'class':'fileclass'}),
        }
        labels={
            'file': '이미지 파일',
        }

AnswerImageFormSet = forms.inlineformset_factory(Answer, AnswerImage, form=AnswerImageForm, extra=3)

class TagForm(forms.Form):
    string = forms.CharField(
        label="태그",
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': '콤마(,) 또는 띄어쓰기로 태그를 구분해 주세요'}),
        )
