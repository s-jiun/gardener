import user
from search.models import Plant, PlantScrap
from django.views.generic.list import ListView
from user.models import GeneralUser, Follow, MyPlant
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileChangeForm, UserAuthenticationForm, UserIdfindForm, MyPlantsForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from community.models import Like
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime


def login(request):
    if request.user.is_authenticated:
        # 수정 요
        return redirect('user:start_page')
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


def signup(request):
    if request.user.is_authenticated:
        # 수정 필요
        return redirect('user:start_page')
    if request.method == 'POST':
        # res = {}
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if age(form.cleaned_data["Date_of_birth"].year, form.cleaned_data["Date_of_birth"].month, form.cleaned_data["Date_of_birth"].day) < 14:
                messages.error(request, "만 14세 이상만 이용가능한 서비스입니다.")
                return redirect('user:signup')

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

    user = request.user

    if request.method == 'POST':
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
            return redirect('user:start_page')

    else:
        user_change_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'user/update.html', {'user_change_form': user_change_form})


@login_required
def profile(request, pk):
    user = GeneralUser.objects.get(id=pk)
    follower = Follow.objects.filter(user=user).count()
    following = Follow.objects.filter(following_user=user).count()
    posts = user.post_set.all().order_by('-id')
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

    rank_user = GeneralUser.objects.annotate(num_resp=Count(
        'following')).order_by('-num_resp')

    ctx = {
        'user': user,
        'rank_user': rank_user[0:5],
        'follower': follower,
        'following': following,
        'posts': page_obj,
        'is_following': is_following,
        'page_obj': page_obj,
    }
    return render(request, template_name='user/profile.html', context=ctx)




@login_required
def follow_list(request, pk):
    user = GeneralUser.objects.get(id=pk)
    followers = user.following.all()
    followings = user.followers.all()
    # user가 팔로잉에 해당하는 팔로우 오브젝트
    cur_users_followings = request.user.followers.all()
    cur_users_followings_list = []
    for cur_users_following in cur_users_followings:
        cur_users_followings_list.append(cur_users_following.user_id)

    ctx = {
        'user': user,
        'followings': followings,
        'followers': followers,
        'cur_users_followings_list': cur_users_followings_list,
        'user': user
    }

    return render(request, template_name='user/follower.html', context=ctx)


@login_required
def profile_update(request):
    user = GeneralUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = UserProfileChangeForm(
            request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.Image = user.Image
            print(user.Image)
            print(form.Image)
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


@login_required
def my_profile(request):
    return redirect('user:profile', pk=request.user.id)


def start_page(request):
    if request.user.is_authenticated:
        if request.user.name == "":
            return redirect('user:profile_update')

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
    return JsonResponse({'user_id': user_id, 'user_userid': user.userid, 'user_name': user.name, 'user_point': user.point, 'user_image_url': user.Image.url})


@csrf_exempt
def follow_ajax(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    user = GeneralUser.objects.get(id=user_id)
    follow = Follow(user=user, following_user=request.user)
    follow.save()
    return JsonResponse({'user_id': user_id, 'user_userid': user.userid, 'user_name': user.name, 'user_point': user.point, 'user_image_url': user.Image.url})


@csrf_exempt
def base_image_ajax(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    user = GeneralUser.objects.get(id=user_id)
    user.Image = '../static/images/default_profile.svg'
    # user.save()
    return JsonResponse({'user_image': user.Image.url})

@csrf_exempt
def save_image_ajax(requset):
    req = json.loads(requset.body)
    user_id = req['user_id']
    src = req['src']
    print('ajax src: ',src)
    user = GeneralUser.objects.get(id=user_id)
    user.Image = '..'+ src
    user.save()
    return JsonResponse({'user_image': user.Image.url})

class liked_post_ListView(ListView):
    model = Like
    paginate_by = 5
    template_name = 'user/my_pick.html'
    context_object_name = 'liked'

    def get_queryset(self):
        user = GeneralUser.objects.get(id=self.kwargs['pk'])
        liked = Like.objects.filter(user_id=user).order_by('-id')
        return liked

    def get_context_data(self, **kwargs):
        follower = Follow.objects.filter(user=self.request.user).count()
        following = Follow.objects.filter(
            following_user=self.request.user).count()
        context = super().get_context_data(**kwargs)
        context["follower"] = follower
        context["following"] = following
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

        return context


class ScrabListView(ListView):
    model = PlantScrap
    paginate_by = 9
    template_name = 'user/my_scrab.html'
    context_object_name = 'scrab_list'

    def get_context_data(self, **kwargs):
        follower = Follow.objects.filter(user=self.request.user).count()
        following = Follow.objects.filter(
            following_user=self.request.user).count()
        context = super().get_context_data(**kwargs)
        context["follower"] = follower
        context["following"] = following
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

        return context

    def get_queryset(self):
        scrab_list = PlantScrap.objects.filter(
            user=self.request.user).order_by('-id')
        return scrab_list


def delete_scrab(request, pk):
    plant = Plant.objects.get(pk=pk)
    scrab = PlantScrap.objects.get(user=request.user, plant=plant)
    scrab.delete()
    return redirect('user:my_scrab_plant', request.user.pk)


class GardenerListView(ListView):
    model = GeneralUser
    paginate_by = 9
    template_name = 'user/search_gardener.html'
    context_object_name = 'gardener_list'

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

        search_keyword = self.request.GET.get('q', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword

        return context

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        gardener_list = GeneralUser.objects.order_by(
            'name').exclude(pk=self.request.user.pk)

        if search_keyword:
            if len(search_keyword) > 1:
                search_gardener_list = gardener_list.filter(
                    userid__icontains=search_keyword).exclude(pk=self.request.user.pk)
                return search_gardener_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return gardener_list


def about(request):
    return render(request, template_name='about.html')


class MyPlantsListView(ListView):
    model = MyPlant
    paginate_by = 12
    template_name = 'user/my_plants.html'
    context_object_name = 'plants_list'

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

        return context

    def get_queryset(self):
        plants_list = MyPlant.objects.filter(
            user=self.request.user).order_by('-id')
        return plants_list


@login_required
def add_myplant(request):
    if request.method == 'POST':
        form = MyPlantsForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant = form.save()
            return redirect('user:my_plants', pk=plant.user.pk)
    else:
        form = MyPlantsForm()
        ctx = {'form': form}
        return render(request, template_name='user/add_myplant.html', context=ctx)
