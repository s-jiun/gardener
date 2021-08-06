from django import forms
from .models import CommunityQuestion, CommunityAnswer
from account.models import GeneralUser


class QuestionForm(forms.ModelForm):
    # user_id = forms.CharField(
    #     label=('user_id'),
    #     widget=forms.TextInput()
    # )
    class Meta:
        model = CommunityQuestion
        # fields = ['user_id', 'title', 'photo', 'content']
        fields = '__all__'


class AnswerForm(forms.ModelForm):
    # title = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput()
    # )
    # # image = forms.ImageField(
    # #     widget=forms.FileInput()
    # # )
    # content = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput()
    # )

    class Meta:
        model = CommunityAnswer
        fields = '__all__'


# from django.forms.fields import EmailField
# from .models import GeneralUser, UserManager
# from django import forms
# from django.contrib.auth.forms import UserChangeForm
# from django.contrib.auth import get_user_model

# class UserCreationForm(forms.ModelForm):
#     # 사용자 생성 폼
#     name = forms.CharField(
#         label=('name'),
#         required=True,
#         widget=forms.TextInput(
#         )
#     )
#     email = forms.EmailField(
#         label=('Email'),
#         required=True,
#         widget=forms.EmailInput(
#         )
#     )
#     userid = forms.CharField(
#         label=('userid'),
#         widget=forms.TextInput()
#     )
#     password1 = forms.CharField(
#         label=('Password'),
#         widget=forms.PasswordInput(

#         )
#     )
#     password2 = forms.CharField(
#         label=('Password confirmation'),
#         widget=forms.PasswordInput(

#         )
#     )

#     class Meta:
#         model = GeneralUser
#         fields = ('name', 'email', 'userid',)

#     def clean_password2(self):
#         # 두 비밀번호 입력 일치 확인
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
#         return password2

#     def clean_email(self):
#         if GeneralUser.objects.filter(email=self.cleaned_data['email']).exists():
#             raise forms.ValidationError('이미 존재하는 이메일입니다.')
#         return self.cleaned_data['email']

#     def clean_userid(self):
#         if GeneralUser.objects.filter(userid=self.cleaned_data['userid']).exists():
#             raise forms.ValidationError('이미 존재하는 아이디입니다.')
#         return self.cleaned_data['userid']

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserCreationForm, self).save(commit=False)
#         user.email = UserManager.normalize_email(self.cleaned_data['email'])
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

# class CustomUserChangeForm(UserChangeForm):
#     password1 = forms.CharField(
#         label=('Password'),
#         widget=forms.PasswordInput(

#         )
#     )
#     password2 = forms.CharField(
#         label=('Password confirmation'),
#         widget=forms.PasswordInput(

#         )
#     )
#     class Meta:
#         model = get_user_model()
#         fields = ['userid', 'email', 'password']

#     def clean_password2(self):
#         # 두 비밀번호 입력 일치 확인
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
#         return password2
