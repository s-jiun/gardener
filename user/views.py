from search.models import Plant, PlantScrap
from django.views.generic.list import ListView
from user.models import GeneralUser, Follow
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileChangeForm, UserAuthenticationForm, UserIdfindForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse_lazy
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from community.models import Like


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
            return redirect('community:post_list')
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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('user:login')
    elif request.method == 'GET':
        form = CustomUserCreationForm()

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
    page = request.GET.get('page', '1')  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(posts, '9')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장

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
        'posts': page_obj,
        'is_following': is_following,
        'page_obj': page_obj,
    }
    return render(request, template_name='user/profile.html', context=ctx)

# class ProfileListView(ListView):
#     model = Post
#     paginate_by = 6
#     # DEFAULT : <app_label>/<model_name>_list.html
#     template_name = 'user/profile.html'
#     context_object_name = 'profile_list'  # DEFAULT : <model_name>_list

#     def get_queryset(self):
#         if request.user.is_authenticated:
#             post_list = request.user.post_set.order_by('-id')
#             return post_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = context['paginator']
#         page_numbers_range = 10
#         max_index = len(paginator.page_range)

#         page = self.request.GET.get('page')
#         current_page = int(page) if page else 1

#         start_index = int((current_page - 1) /
#                           page_numbers_range) * page_numbers_range
#         end_index = start_index + page_numbers_range
#         if end_index >= max_index:
#             end_index = max_index

#         page_range = paginator.page_range[start_index:end_index]
#         context['page_range'] = page_range

#         return context


# def follower_list(request, pk):

#     user = GeneralUser.objects.get(id=pk)
#     # user가 팔로잉에 해당하는 팔로우 오브젝트
#     followers = user.following.all()
#     cur_users_followings = request.user.followers.all()
#     cur_users_followings_list = []
#     for cur_users_following in cur_users_followings:
#         cur_users_followings_list.append(cur_users_following.user_id)

#     ctx = {
#         'followers': followers,
#         'cur_users_followings_list': cur_users_followings_list
#     }

#     return render(request, template_name='user/follower.html', context=ctx)


# def following_list(request, pk):
#     user = GeneralUser.objects.get(id=pk)
#     # user가 팔로워에 해당하는 팔로우 오브젝트
#     followings = user.followers.all()
#     cur_users_followings = request.user.followers.all()
#     cur_users_followings_list = []
#     for cur_users_following in cur_users_followings:
#         cur_users_followings_list.append(cur_users_following.user_id)

#     ctx = {
#         'followings': followings,
#         'cur_users_followings_list': cur_users_followings_list
#     }

#     return render(request, template_name='user/following.html', context=ctx)

def follow_list(request, pk):
    user = GeneralUser.objects.get(id=pk)
    # user가 팔로잉에 해당하는 팔로우 오브젝트
    followers = user.following.all()
    followings = user.followers.all()
    cur_users_followings = request.user.followers.all()
    cur_users_followings_list = []
    for cur_users_following in cur_users_followings:
        cur_users_followings_list.append(cur_users_following.user_id)

    ctx = {
        'followings': followings,
        'followers': followers,
        'cur_users_followings_list': cur_users_followings_list
    }

    return render(request, template_name='user/follower.html', context=ctx)


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


def start_page(request):
    return render(request, template_name='welcome.html')


def find_id(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = GeneralUser.objects.get(email=email)
            ctx = {
                'user': user,
                'email': email
            }
            return render(request, template_name='user/find_id_done.html', context=ctx)
        except:
            ctx = {
                'email': email
            }
            return render(request, template_name='user/find_id_fail.html', context=ctx)

    else:
        form = UserIdfindForm()
        ctx = {
            'form': form
        }
    return render(request, template_name='user/find_id.html', context=ctx)


@csrf_exempt
def following_ajax(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    user = GeneralUser.objects.get(id=user_id)
    following = Follow.objects.filter(user_id=user_id).filter(
        following_user=request.user.id)
    following.delete()
    return JsonResponse({'user_id': user_id, 'user_userid':user.userid,'user_name':user.name, 'user_point':user.point, 'user_image_url':user.Image.url})


@csrf_exempt
def follow_ajax(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    user = GeneralUser.objects.get(id=user_id)
    follow = Follow(user=user, following_user=request.user)
    follow.save()
    return JsonResponse({'user_id': user_id, 'user_userid':user.userid,'user_name':user.name, 'user_point':user.point, 'user_image_url':user.Image.url})

# @csrf_exempt
# def follow_list_ajax(request):
#     req = json.load(request.body)
#     user_id = req['user_id']
#     user = GeneralUser.objects.get(id=user_id)
    

def liked_posts(request, pk):
    user = GeneralUser.objects.get(id=pk)
    liked = Like.objects.filter(user_id=user)
    print(liked)
    ctx = {'liked': liked, 'user': user}
    return render(request, 'user/my_pick.html', context=ctx)


class liked_post_ListView(ListView):
    model = Like
    paginate_by = 5
    template_name = 'user/my_pick.html'
    context_object_name = 'liked'

    def get_queryset(self):
        user = GeneralUser.objects.get(id=self.kwargs['pk'])
        liked = Like.objects.filter(user_id=user).order_by('id')
        return liked

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) /
                          page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]

        context['user'] = GeneralUser.objects.get(id=self.kwargs['pk'])
        context['page_range'] = page_range
        return context


class ScrabListView(ListView):
    model = PlantScrap
    paginate_by = 9
    template_name = 'user/my_scrab.html'
    context_object_name = 'scrab_list'  # DEFAULT : <model_name>_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) /
                          page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        # search_keyword = self.request.GET.get('q', '')

        # if len(search_keyword) > 1:
        #     context['q'] = search_keyword

        return context

    def get_queryset(self):
        scrab_list = PlantScrap.objects.filter(user=self.request.user)
        return scrab_list


def delete_scrab(request, pk):
    plant = Plant.objects.get(pk=pk)
    scrab = PlantScrap.objects.get(user=request.user, plant=plant)
    scrab.delete()
    return redirect('user:my_scrab_plant', request.user.pk)
