from account.models import GeneralUser
import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments, TaggedPost, Image

from .forms import PostForm, ImageFormSet
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.generic import ListView
from django.contrib import messages
# Create your views here.


class PostListView(ListView):
    model = Post
    paginate_by = 10
    # DEFAULT : <app_label>/<model_name>_list.html
    template_name = 'community/post_list.html'
    context_object_name = 'post_list'  # DEFAULT : <model_name>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        post_list = Post.objects.order_by('-id')
        if search_keyword:
            if len(search_keyword) > 1:
                search_post_list = post_list.filter(
                    tags__name=search_keyword)
                return search_post_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return post_list

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


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comments.objects.filter(post_id=pk)
    images = Image.objects.filter(post=post)
    ctx = {'post': post, 'images': images, 'comments': comments}
    return render(request, template_name='community/post_detail.html', context=ctx)


@login_required
def post_create(request, post=None):
    if request.method == 'POST':

        form = PostForm(request.POST,instance=post)
        image_formset = ImageFormSet(request.POST, request.FILES, instance =post)

        if form.is_valid() and image_formset.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            with transaction.atomic():
                post = form.save()
                image_formset.instance = post
                image_formset.save()

            # form.save_m2m()
                return redirect('community:post_detail', pk=post.pk)
        else:
            ctx = {'form': form, 'is_create': 0,
                   'image_formset': image_formset}
            return render(request, template_name='community/post_form.html', context=ctx)
    elif request.method == 'GET':
        form = PostForm(instance=post)
        image_formset = ImageFormSet(instance=post)
        ctx = {'form': form, 'is_create': 0, 'image_formset': image_formset}

    return render(request, template_name='community/post_form.html', context=ctx)


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return post_create(request, post=post)


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


def search_tag(request):
    if request.method == 'POST':
        keyword = request.POST.get('search')

        posts = TaggedPost.objects.filter(tag=keyword).values('content_object')

        ctx = {'posts': posts}
        return render(request, template_name='community/search_post.html', context=ctx)

    elif request.method == 'GET':
        return redirect('community:post_list')
