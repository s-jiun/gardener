from django import forms
from .models import CommunityQuestion, CommunityAnswer
from account.models import GeneralUser


class QuestionForm(forms.ModelForm):

    class Meta:
        model = CommunityQuestion
        fields = '__all__'


class AnswerForm(forms.ModelForm):

    class Meta:
        model = CommunityAnswer
        fields = '__all__'
