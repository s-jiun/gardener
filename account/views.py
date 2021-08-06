import django
from django.db.models.query import InstanceCheckMeta
from django.http import request
from account.models import GeneralUser, Follow
from django.shortcuts import render, redirect
from .forms import UserCreationForm, CustomUserChangeForm, UserProfileChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
    if request.user.is_authenticated:
        ## 수정 요
         return redirect('account:update')
    if request.method == 'POST':
        # 사용자가 보낸 값 -> form
        form = AuthenticationForm(request, request.POST)
        # 검증
        if form.is_valid():
            # 검증 완료시 로그인!
            auth_login(request, form.get_user())
            return redirect('/')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)

def logout(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    auth_logout(request)
    return redirect('/')

def signup(request):
    if request.user.is_authenticated:
        # 수정 필요
        return redirect('account:update')
    if request.method == 'POST':
        res = {}
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('account:login')
    elif request.method == 'GET':
        form = UserCreationForm()
    
    return render(request, 'account/signup.html', {'form':form})
    
def member_del(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('/')
    return render(request, template_name='account/signout.html')


def member_modification(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user = user_change_form.save(commit = False)
            user.set_password(user_change_form.cleaned_data['password1'])
            user.save()
            return redirect('/', request.user.userid)
    
    else:
	    user_change_form = CustomUserChangeForm(instance = request.user)

    return render(request, 'account/update.html', {'user_change_form':user_change_form})

def profile(request, pk):
    user = GeneralUser.objects.get(id=pk)
    follower = Follow.objects.filter(user=user).count()
    following = Follow.objects.filter(following_user=user).count()
    posts = user.post_set.all()
    ctx = {
        'user':user,
        'follower': follower,
        'following':following,
        'posts':posts
    }
    return render(request, template_name='account/profile.html', context=ctx)
def follower_list(request,pk):
    
    user = GeneralUser.objects.get(id=pk)
    # user가 팔로잉에 해당하는 팔로우 오브젝트
    followers = user.following.all()

    ctx = {
        'followers':followers
    }

    return render(request, template_name='account/follower.html',context=ctx)

def following_list(request,pk):
    user = GeneralUser.objects.get(id=pk)
    # user가 팔로워에 해당하는 팔로우 오브젝트 
    followings = user.followers.all()
    ctx = {
        'followings':followings
    }

    return render(request, template_name='account/following.html',context=ctx)

def profile_update(request):
    user = GeneralUser.objects.get(id = request.user.id)
    if request.method == 'POST':
        form = UserProfileChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            follower = Follow.objects.filter(user=user).count()
            following = Follow.objects.filter(following_user=user).count()
    
            ctx = {
               'user':request.user,
               'follower':follower,
               'following':following, 
            }
            return redirect('account:profile',pk=request.user.id)
    else:
        form = UserProfileChangeForm(instance=request.user)
        ctx = {
            'form':form
        }
    return render(request, template_name='account/profile_update.html', context=ctx)

def my_profile(request):
    return redirect('account:profile',pk=request.user.id)

def main_page(request):
    pass

def start_page(request):
    pass