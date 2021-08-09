from django import forms

from .models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = '__all__'
# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['files']


# ImageFormSet = forms.inlineformset_factory(
#     Post, Image, form=ImageForm, extra=4)
