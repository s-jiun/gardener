
from django import forms

from .models import Challenge, ChallengeReply,CardNews,NewsReply


class ChallengeReplyForm(forms.ModelForm):
    class Meta:
        model = ChallengeReply
        fields = ['content']