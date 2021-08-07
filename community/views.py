from account.models import GeneralUser
import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments, TaggedPost, Image
from .forms import ImageForm, PostForm, ImageFormSet
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction


# Create your views here.


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    images = Image.objects.all()
    ctx = {'posts': posts, 'images': images}
    return render(request, template_name='community/post_list.html', context=ctx)


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comments.objects.filter(post_id=pk)
    images = Image.objects.filter(post=post)
    ctx = {'post': post, 'images': images, 'comments': comments}
    return render(request, template_name='community/post_detail.html', context=ctx)


@login_required
def post_create(request, post=None):
    if request.method == 'POST':
        form = PostForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)
        if form.is_valid() and image_formset.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            with transaction.atomic():
                post = form.save()
                image_formset.instance = post
                image_formset.save()
                return redirect('community:post_detail', pk=post.pk)
        else:
            ctx = {'form': form, 'image_formset': image_formset, 'is_create': 0}
            return render(request, template_name='community/post_form.html', context=ctx)
    elif request.method == 'GET':
        form = PostForm()
        image_formset = ImageFormSet()
        ctx = {'form': form, 'image_formset': image_formset, 'is_create': 0}

    return render(request, template_name='community/post_form.html', context=ctx)


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        image_formset = ImageFormSet(
            request.POST, request.FILES, instance=post)
        if form.is_valid() and image_formset.is_valid():
            post = form.save(commit=False)
            post.tags.clear()
            with transaction.atomic():
                post = form.save()
                image_formset.instance = post
                image_formset.save()
                return redirect('community:post_detail', pk=post.pk)
        else:
            ctx = {'form': form, 'image_formset': image_formset, 'is_create': 1}
            return render(request, template_name='community/post_form.html', context=ctx)
    elif request.method == 'GET':
        form = PostForm(instance=post)
        image_formset = ImageFormSet(instance=post)
        ctx = {'form': form, 'image_formset': image_formset, 'is_create': 1}
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


def search_tag(request):
    if request.method == 'POST':
        keyword = request.POST.get('search')
        posts = TaggedPost.objects.filter(tag=keyword).values('content_object')

        ctx = {'posts': posts}
        return render(request, template_name='community/search_post.html', context=ctx)

    elif request.method == 'GET':
        return redirect('community:post_list')
