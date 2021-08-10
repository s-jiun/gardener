from django.core.mail.message import EmailMessage
import django
from django.db.models.query import InstanceCheckMeta
from django.http import request
from user.models import GeneralUser, Follow
from django.shortcuts import render, redirect
from .forms import UserCreationForm, CustomUserChangeForm, UserProfileChangeForm, UserAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView,PasswordResetView
from django.urls import reverse_lazy
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)


def login(request):
    if request.user.is_authenticated:
        # 수정 요
        return redirect('user:update')
    if request.method == 'POST':
        # 사용자가 보낸 값 -> form
        form = UserAuthenticationForm(request, request.POST)
        # 검증
        if form.is_valid():
            # 검증 완료시 로그인!
            auth_login(request, form.get_user())
            return redirect('/')
    else:
        form = UserAuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)


def logout(request):
    if not request.user.is_authenticated:
        return redirect('user:login')
    auth_logout(request)
    return redirect('/')


def signup(request):
    if request.user.is_authenticated:
        # 수정 필요
        return redirect('user:update')
    if request.method == 'POST':
        res = {}
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('user:login')
    elif request.method == 'GET':
        form = UserCreationForm()

    return render(request, 'user/signup.html', {'form': form})


def member_del(request):
    if not request.user.is_authenticated:
        return redirect('user:login')
    if request.method == 'POST':
        user = request.user
        user.delete()
        return render(request, template_name='user/signout_done.html')
    return render(request, template_name='user/signout.html')


def member_modification(request):
    if not request.user.is_authenticated:
        return redirect('user:login')
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(
            request.POST, instance=request.user)
        if user_change_form.is_valid():
            user = user_change_form.save(commit=False)
            user.set_password(user_change_form.cleaned_data['password1'])
            user.save()
            return redirect('/', request.user.userid)

    else:
        user_change_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'user/update.html', {'user_change_form': user_change_form})


def profile(request, pk):
    user = GeneralUser.objects.get(id=pk)
    follower = Follow.objects.filter(user=user).count()
    following = Follow.objects.filter(following_user=user).count()
    posts = user.post_set.all()
    login_user_followings = Follow.objects.filter(
        following_user=request.user.id)
    is_following = False
    for i in login_user_followings:
        if user.id == i.user_id:
            is_following = True
            break

    ctx = {
        'user': user,
        'follower': follower,
        'following': following,
        'posts': posts,
        'is_following': is_following
    }
    return render(request, template_name='user/profile.html', context=ctx)


def follower_list(request, pk):

    user = GeneralUser.objects.get(id=pk)
    # user가 팔로잉에 해당하는 팔로우 오브젝트
    followers = user.following.all()
    cur_users_followings = request.user.followers.all()
    cur_users_followings_list = []
    for cur_users_following in cur_users_followings:
        cur_users_followings_list.append(cur_users_following.user_id)

    ctx = {
        'followers': followers,
        'cur_users_followings_list': cur_users_followings_list
    }

    return render(request, template_name='user/follower.html', context=ctx)


def following_list(request, pk):
    user = GeneralUser.objects.get(id=pk)
    # user가 팔로워에 해당하는 팔로우 오브젝트
    followings = user.followers.all()
    cur_users_followings = request.user.followers.all()
    cur_users_followings_list = []
    for cur_users_following in cur_users_followings:
        cur_users_followings_list.append(cur_users_following.user_id)

    ctx = {
        'followings': followings,
        'cur_users_followings_list': cur_users_followings_list
    }

    return render(request, template_name='user/following.html', context=ctx)


def profile_update(request):
    user = GeneralUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = UserProfileChangeForm(
            request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            follower = Follow.objects.filter(user=user).count()
            following = Follow.objects.filter(following_user=user).count()

            ctx = {
                'user': request.user,
                'follower': follower,
                'following': following,
            }
            return redirect('user:profile', pk=request.user.id)
    else:
        form = UserProfileChangeForm(instance=request.user)
        ctx = {
            'form': form
        }
    return render(request, template_name='user/profile_update.html', context=ctx)


def my_profile(request):
    return redirect('user:profile', pk=request.user.id)


def main_page(request):
    pass


def start_page(request):
    pass


@csrf_exempt
def following_ajax(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    following = Follow.objects.filter(user_id=user_id).filter(
        following_user=request.user.id)
    following.delete()
    return JsonResponse({'user_id': user_id})


@csrf_exempt
def follow_ajax(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    user = GeneralUser.objects.get(id=user_id)
    follow = Follow(user=user, following_user=request.user)
    follow.save()
    return JsonResponse({'user_id':user_id})