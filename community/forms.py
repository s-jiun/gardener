from django import forms
from .models import Post, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['files']


ImageFormSet = forms.inlineformset_factory(
    Post, Image, form=ImageForm, extra=4)
