
from django import forms
from django.db.models import fields

from .models import Challenge, ChallengeReply, CardNews, NewsReply


class ChallengeReplyForm(forms.ModelForm):
    class Meta:
        model = ChallengeReply
        fields = ['content']


class NewsReplyForm(forms.ModelForm):

    class Meta:
        model = NewsReply
        fields = ['content']
