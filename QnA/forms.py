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
        fields = ['title', 'content', 'tags']


class AnswerForm(forms.ModelForm):

    class Meta:
        model = CommunityAnswer
        fields = ['title', 'content']
