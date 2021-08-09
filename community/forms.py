from django import forms

from .models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
