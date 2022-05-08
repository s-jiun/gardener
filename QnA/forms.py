from django import forms
from taggit.forms import TagWidget
from .models import CommunityQuestion, CommunityAnswer
from user.models import GeneralUser


class QuestionForm(forms.ModelForm):

    widgets = {
        'tags': TagWidget(),
    }

    class Meta:
        model = CommunityQuestion
        fields = ['content', 'tags']
        labels = {
            'tags': '태그(#리시안셔스 #라넌큘러스 #무궁화 -> 띄어쓰기로 구분해주세요!!)',
        }


class AnswerForm(forms.ModelForm):

    class Meta:
        model = CommunityAnswer
        fields = ['content']
