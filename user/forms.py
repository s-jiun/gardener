from unicodedata import name
from urllib import request
from django.core.exceptions import ValidationError
from .models import GeneralUser, UserManager, MyPlant
from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from allauth.account.forms import SignupForm
from datetime import datetime


class UserAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control', 'placeholder': '아이디'}))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control', 'placeholder': '비밀번호'}),
    )

    def clean_password(self):
        username = self.cleaned_data.get('username') # 우리가 입력한 값
        password = self.cleaned_data.get('password')
        
        if username is not None:
            if authenticate(self.request, username=username, password=password) is not None:
                return password
            else:
                user = GeneralUser.objects.get(userid=username)
                if(user.is_active == False):
                    raise ValidationError('이메일 인증을 완료해주세요!')
                else:
                    if(user.userid != username):
                        raise ValidationError('아이디가 없습니다.')
                    else:
                        raise ValidationError('비밀번호가 일치하지 않습니다!')



Year_choices = list()
for i in range(1900, 2022):
    Year_choices.append(i)
Month_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def age(birth_year, birth_month, birth_day):
    now = datetime.now()
    if birth_month < now.year:
        return now.year - birth_year
    elif birth_month == now.month:
        if birth_day <= now.day:
            return now.year - birth_year
        else:
            return now.year - birth_year - 1
    else:
        return now.year - birth_year - 1


class CustomUserCreationForm(UserCreationForm):
    # 사용자 생성 폼
    name = forms.CharField(
        label=('name'),
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'signup-form-control'}
        )
    )
    email = forms.EmailField(
        label=('Email'),
        required=True,
        widget=forms.DateInput(
            attrs={'class': 'signup-form-control'})
    )
    userid = forms.CharField(
        label=('userid'),
        widget=forms.TextInput(
            attrs={'class': 'signup-form-control'})
    )

    Date_of_birth = forms.DateField(
        label=("Birth"),
        required=True,
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            years=Year_choices,
            attrs={'class': 'signup-form-control'}
        )
    )

    class Meta:
        model = GeneralUser
        fields = ('name', 'email', 'userid', 'Date_of_birth')

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

    

    # def clean_Date_of_birth(self):
    #     if age(self.cleaned_data['Date_of_birth'].year, self.cleaned_data['Date_of_birth'].month, self.cleaned_data['Date_of_birth'].day) < 14:
    #         raise forms.ValidationError('만 14세 이상만 이용가능한 서비스입니다.')
    #     return self.cleaned_data['Date_of_birth']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    userid = forms.CharField(
        label=('Userid'),
        widget=forms.TextInput(
            attrs={'class': 'update-form-control'}

        )
    )
    email = forms.EmailField(
        label=('Email'),
        widget=forms.EmailInput(
            attrs={'class': 'update-form-control'}

        )
    )

    Date_of_birth = forms.DateField(
        label=("Birth"),
        required=True,
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            years=Year_choices,
            attrs={'class': 'signup-form-control'}
        )
    )

    password1 = forms.CharField(
        label=('Password'),
        widget=forms.PasswordInput(
            attrs={'class': 'update-form-control'}

        )
    )
    password2 = forms.CharField(
        label=('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={'class': 'update-form-control'}

        )
    )

    class Meta:
        model = get_user_model()
        fields = ['userid', 'email', 'password', 'Date_of_birth']

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2


class UserProfileChangeForm(UserChangeForm):

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


class UserIdfindForm(forms.ModelForm):
    email = forms.EmailField(
        label=('Email'),
        widget=forms.EmailInput(
            attrs={'class': 'update-form-control'}

        )
    )

    class Meta:
        model = GeneralUser
        fields = ['email']


class MyPlantsForm(forms.ModelForm):
    class Meta:
        model = MyPlant
        fields = ['plant_name', 'Image']
