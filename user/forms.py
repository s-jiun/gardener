from django.db import models
from django.forms.fields import EmailField
from .models import GeneralUser, UserManager
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm

class UserCreationForm(forms.ModelForm):
    # 사용자 생성 폼
    name = forms.CharField(
        label=('name'),
        required=True,
        widget=forms.TextInput(
        )
    )
    email = forms.EmailField(
        label=('Email'),
        required=True,
        widget=forms.EmailInput(
        )
    )
    userid = forms.CharField(
        label=('userid'),
        widget=forms.TextInput()
    )
    password1 = forms.CharField(
        label=('Password'),
        widget=forms.PasswordInput(
            
        )
    )
    password2 = forms.CharField(
        label=('Password confirmation'),
        widget=forms.PasswordInput(
            
        )
    )

    class Meta:
        model = GeneralUser
        fields = ('name', 'email', 'userid',)

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def clean_email(self):
        if GeneralUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('이미 존재하는 이메일입니다.')
        return self.cleaned_data['email']

    def clean_userid(self):
        if GeneralUser.objects.filter(userid=self.cleaned_data['userid']).exists():
            raise forms.ValidationError('이미 존재하는 아이디입니다.')
        return self.cleaned_data['userid']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(
        label=('Password'),
        widget=forms.PasswordInput(
            
        )
    )
    password2 = forms.CharField(
        label=('Password confirmation'),
        widget=forms.PasswordInput(
            
        )
    )
    class Meta:
        model = get_user_model()
        fields = ['userid', 'email', 'password']
    
    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

class UserProfileChangeForm(UserChangeForm):
    Image = forms.ImageField(
        label=('image'),
        required=False,
        widget=forms.FileInput()
    )
    name = forms.CharField(
        label=('name'),
        required=True,
        widget=forms.TextInput(
        )
    )
    profile = forms.CharField(
        label=('profile'),
        required=False
    )
    class Meta:
        model = get_user_model()
        fields = ['Image', 'name', 'profile']

class MyCustomSignupForm(SignupForm):
    agree_terms = forms.BooleanField(label='서비스 이용약관 및 개인정보방침 동의')
    agree_marketing = forms.BooleanField(label='마케팅 이용 동의')

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.agree_terms = self.cleaned_data['agree_terms']
        user.agree_marketing = self.cleaned_data['agree_marketing']
        user.save()
        return user