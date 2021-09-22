from django.contrib.auth import authenticate
from user.models import Follow, GeneralUser
import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Reply, Postviews, Notice, Noticetviews, TaggedPost
from taggit.models import Tag
from .forms import PostForm, ReplyForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q


class PostListView(ListView):
    model = Post
    paginate_by = 9
    template_name = 'community/post_list.html'
    context_object_name = 'post_list'

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
        
        # user= self.request.user;

        # liked_user = Like.objects.filter(
        # post_id=user.pk).values_list('user_id', flat=True)


        if len(search_keyword) > 1:
            context['q'] = search_keyword

        return context

    def get_queryset(self):

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        post_list = Post.objects.order_by('-id')
        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'tag':
                    search_post_list = post_list.filter(
                        Q(tags__name=search_keyword))
                elif search_type == 'title':
                    search_post_list = post_list.filter(
                        Q(title__icontains=search_keyword))
                elif search_type == 'content':
                    search_post_list = post_list.filter(
                        Q(content__icontains=search_keyword))
                return search_post_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return post_list


class FollowPostView(ListView):
    model = Post
    paginate_by = 9
    template_name = 'community/follow_post_list.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        context['followings'] = Follow.objects.filter(
            following_user=self.request.user.id)
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
        search_type = self.request.GET.get('type', '')

        followings = Follow.objects.filter(following_user=self.request.user.id)
        post_list = []
        following_list = []
        for following in followings:
            following_list.append(following.user_id)

        post_list = Post.objects.filter(user_id__in=following_list)

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'tag':
                    search_post_list = post_list.filter(
                        Q(tags__name=search_keyword))
                elif search_type == 'title':
                    search_post_list = post_list.filter(
                        Q(title__icontains=search_keyword))
                elif search_type == 'content':
                    search_post_list = post_list.filter(
                        Q(content__icontains=search_keyword))
                return search_post_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return post_list

# 사용자 ip 주소 받아오는 함수


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Postviews.objects.get_or_create(
        post=post, client_ip=get_client_ip(request))

    comments = post.reply_set.filter(parent_reply__isnull=True)
    comments_num = comments.count()
    liked_user = Like.objects.filter(
        post_id=pk).values_list('user_id', flat=True)
    is_following = False
    user_id = post.user_id.id
    followers = Follow.objects.filter(user_id=user_id)
    for follower in followers:
        if request.user.id == follower.following_user_id:
            is_following = True
            break

    if request.method == 'POST':
        comment_form = ReplyForm(request.POST, request.FILES)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Reply.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent_reply = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.post_id = post

            new_comment.user_id = GeneralUser.objects.get(
                userid=request.user.get_username())
            new_comment.save()
            return redirect('community:post_detail', pk=post.pk)
    else:
        comment_form = ReplyForm()
    return render(request,
                'community/post_detail.html',
                {'post': post,
                'comments': comments,
                'comments_num' : comments_num,
                'comment_form': comment_form,
                'liked_user': liked_user,
                'is_following': is_following,
                'views': len(Postviews.objects.filter(post=post))})


@login_required
def post_create(request, post=None):
    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post = form.save()
            request.user.point += 30
            request.user.save()
            return redirect('community:post_detail', pk=post.pk)
        else:
            ctx = {'form': form, 'is_post': post}
            return render(request, template_name='community/post_form.html', context=ctx)
    elif request.method == 'GET':
        form = PostForm()
        ctx = {'form': form, 'is_post': post}

    return render(request, template_name='community/post_form.html', context=ctx)


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post = form.save()
            return redirect('community:post_detail', pk=post.pk)
        else:
            ctx = {'form': form, 'is_post': post}
            return render(request, template_name='community/post_form.html', context=ctx)
    elif request.method == 'GET':
        form = PostForm(instance=post)
        pk = post.pk
        ctx = {'form': form, 'is_post': post, 'pk': pk}

    return render(request, template_name='community/post_form.html', context=ctx)


@login_required
def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    tagged_posts = TaggedPost.objects.filter(content_object_id=pk)
    for tagged_post in tagged_posts:
        tag_id = tagged_post.tag_id
        tag = Tag.objects.get(id=tag_id)
        if TaggedPost.objects.filter(tag_id=tag_id).count() > 1:
            pass
        else:
            tag.delete()

    post.delete()
    return redirect('community:post_list')


@login_required
@csrf_exempt
def delete_reply(request, pk):
    req = json.loads(request.body)
    post_id = req['post_id']
    parent_id = req['parent_id']
    reply_id = req['reply_id']
    if parent_id != None:
        parent_obj = Reply.objects.get(post_id=post_id, id=parent_id)
        Reply.objects.get(
            post_id=post_id, parent_reply=parent_obj, id=reply_id).delete()
    else:
        comment = Reply.objects.get(post_id=post_id, id=reply_id)
        Reply.objects.filter(post_id=post_id, parent_reply=comment).delete()
        comment.delete()

    return JsonResponse({'parent_id': parent_id, 'post_id': post_id, 'reply_id': reply_id})


@login_required
@csrf_exempt
def delete_comment(request, pk):
    req = json.loads(request.body)
    post_id = req['post_id']
    comment_id = req['comment_id']

    comment = Reply.objects.get(post_id=post_id, id=comment_id)
    Reply.objects.filter(post_id=post_id, parent_reply=comment).delete()
    comment.delete()

    return JsonResponse({'post_id': post_id, 'comment_id': comment_id})


@login_required
@csrf_exempt
def like_ajax(request,pk):
    print("post_like")
    req = json.loads(request.body)
    post_id = req['id']
    post = Post.objects.get(id=post_id)
    if(Like.objects.filter(user_id=request.user, post_id=post).count() != 0):
        Like.objects.get(user_id=request.user, post_id=post).delete()
    else:
        Like.objects.create(user_id=request.user, post_id=post)

    like_count = Like.objects.filter(post_id=post).count()
    post.save()
    return JsonResponse({'id': post_id, 'like_count': like_count})


class tagListView(ListView):
    model = Post
    paginate_by = 4
    template_name = 'community/tagged_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(
            tags__name=self.kwargs['tag']).order_by('id')
        return posts

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

        context['tag'] = self.kwargs['tag']
        context['page_range'] = page_range
        return context


class NoticeListView(ListView):
    model = Notice
    paginate_by = 9
    template_name = 'community/notice.html'
    context_object_name = 'notice'

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
        search_type = self.request.GET.get('type', '')
        notice_list = Notice.objects.order_by('-id')
        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'tag':
                    search_notice_list = notice_list.filter(
                        Q(tags__name=search_keyword))
                elif search_type == 'title':
                    search_notice_list = notice_list.filter(
                        Q(title__icontains=search_keyword))
                elif search_type == 'content':
                    search_notice_list = notice_list.filter(
                        Q(content__icontains=search_keyword))
                return search_notice_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return notice_list


def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if not Noticetviews.objects.filter(client_ip=get_client_ip(request)):
        Noticetviews.objects.create(
            notice=notice, client_ip=get_client_ip(request))

    ctx = {'notice': notice, 'views': len(
        Noticetviews.objects.filter(notice=notice))}

    return render(request, template_name='community/notice_detail.html', context=ctx)
