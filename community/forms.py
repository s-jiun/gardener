from django import forms
import json
from .models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
