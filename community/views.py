from user.models import Follow, GeneralUser
import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments, Like, Reply

from .forms import PostForm, ReplyForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q


class PostListView(ListView):
    model = Post
    paginate_by = 9
    # DEFAULT : <app_label>/<model_name>_list.html
    template_name = 'community/post_list.html'
    context_object_name = 'post_list'  # DEFAULT : <model_name>_list

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


def post_detail(request, pk):
    # get post object
    post = get_object_or_404(Post, pk=pk)
    # list of active parent comments
    comments = post.reply_set.filter(parent_reply__isnull=True)
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
        # comment has been added
        comment_form = ReplyForm(request.POST, request.FILES)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Reply.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent_reply = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.post_id = post

            new_comment.user_id = GeneralUser.objects.get(
                userid=request.user.get_username())
            # save
            new_comment.save()
            return redirect('community:post_detail', pk=post.pk)
    else:
        comment_form = ReplyForm()
    return render(request,
                  'community/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'liked_user': liked_user,
                   'is_following':is_following})


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
    post.delete()
    return redirect('community:post_list')


@login_required
@csrf_exempt
def add_comment(request, pk):
    req = json.loads(request.body)
    post_id = req['id']
    comment_content = req['ct']
    comment = Comments()
    comment.user_id = get_object_or_404(
        GeneralUser, userid=request.user.get_username())
    comment.post_id = get_object_or_404(Post, pk=pk)
    comment.content = comment_content
    comment.save()
    return JsonResponse({'id': post_id, 'ct': comment_content, 'comment_id': comment.pk})


@login_required
@csrf_exempt
def delete_comment(request, pk):
    req = json.loads(request.body)
    post_id = req['post_id']
    comment_id = req['comment_id']

    Comments.objects.get(post_id=post_id, id=comment_id).delete()

    return JsonResponse({'comment_id': comment_id, 'post_id': post_id})


@login_required
@csrf_exempt
def like_ajax(request, pk):
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


def search_tag(request, tag):

    posts = Post.objects.filter(tags__name=tag)
    ctx = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'community/tagged_list.html', context=ctx)
