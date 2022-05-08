from django import forms
import json
from .models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content','tags']
        labels = {
            'tags': '태그(#리시안셔스 #라넌큘러스 #무궁화 -> 띄어쓰기로 구분해주세요!!)',
        }



class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

