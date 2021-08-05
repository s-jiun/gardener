import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments, Tag, TaggedPost
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    ctx = {'posts': posts}
    return render(request, template_name='post_list.html', context=ctx)


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    ctx = {'post': post}
    return render(request, template_name='post_detail.html', context=ctx)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            form.save_m2m()
            return redirect('Posts:post_detail')
    else:
        form = PostForm()
        ctx = {'form': form}

        return render(request, template_name='post_form.html', context=ctx)


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = PostForm(request.Post, instance=post)
        if form.is_valid():
            post.tags.clear()
            post = form.save()
            form.save_m2m()
            return redirect('Post:post_detail', pk)
    else:
        form = PostForm(instance=post)
        ctx = {'form': form}
    return render(request, template_name='post_form.html', context=ctx)


@login_required
def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('Post:post_list')


@login_required
@csrf_exempt
def add_comment(request):
    print('view')
    req = json.loads(request.body)
    post_id = req['id']
    content = req['content']
    post = Post.objects.get(id=post_id)
    comment = Comments.objects.create(board=post, text=content)

    post.save()
    return JsonResponse({'post_id': post_id, 'comment_id': comment.id, 'content': comment.text})


@login_required
@csrf_exempt
def delete_comment(request):
    req = json.loads(request.body)
    post_id = req['post_id']
    comment_id = req['comment_id']
    post = Post.objects.get(id=post_id)
    Comments.objects.get(board=post, id=comment_id).delete()

    post.save()
    return JsonResponse({'post_id': post_id, 'comment_id': comment_id})


def search_tag(request):
    if request.method == 'POST':
        keyword = request.POST.get('search')
        posts = TaggedPost.objects.filter(tag=keyword).values('content_object')

        ctx = {'posts': posts}
        return render(request, template_name='search_post.html', context=ctx)

    elif request.method == 'GET':
        return redirect('Post:post_list')
