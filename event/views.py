from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from user.models import Follow, GeneralUser
from .models import Challenge, CardNews, ChallengeReply, NewsReply, Challengeviews
from .forms import ChallengeReplyForm
import json
from django.http.response import JsonResponse

# Create your views here.


class ChallengeListView(ListView):
    model = Challenge
    paginate_by = 9
    template_name = 'event/challenge_list.html'
    context_object_name = 'challenge_list'

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
        challenge_list = Challenge.objects.order_by('-id')
        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'type':
                    search_challenge_list = challenge_list.filter(
                        Q(type=search_keyword))
                elif search_type == 'title':
                    search_challenge_list = challenge_list.filter(
                        Q(title__icontains=search_keyword))
                elif search_type == 'content':
                    search_challenge_list = challenge_list.filter(
                        Q(content__icontains=search_keyword))
                return search_challenge_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return challenge_list


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    if not Challengeviews.objects.filter(client_ip=get_client_ip(request)):
        Challengeviews.objects.create(
            challenge=challenge, client_ip=get_client_ip(request))

    comments = challenge.challengereply_set.filter(parent_reply__isnull=True)
    comment_count = ChallengeReply.objects.filter(challenge_id=pk).count()

    if request.method == 'POST':
        comment_form = ChallengeReplyForm(request.POST, request.FILES)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = ChallengeReply.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent_reply = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.challenge_id = challenge

            new_comment.user_id = GeneralUser.objects.get(
                userid=request.user.get_username())
            new_comment.save()
            return redirect('event:challenge_detail', pk=challenge.pk)
    else:
        comment_form = ChallengeReplyForm()

    ctx = {
        'challenge': challenge,
        'comments': comments,
        'comment_form': comment_form,
        'comment_count': comment_count,
        'views': len(
            Challengeviews.objects.filter(challenge=challenge)),
    }
    return render(request, 'event/challenge_detail.html', context=ctx)


class NewsListView(ListView):
    model = CardNews
    paginate_by = 9
    template_name = 'event/issue_list.html'
    context_object_name = 'issue_list'

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
        issue_list = CardNews.objects.order_by('-id')
        if search_keyword:
            if len(search_keyword) > 1:
                return issue_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return issue_list


def issue_detail(request, pk):
    issue = get_object_or_404(CardNews, pk=pk)
    ctx = {
        'issue': issue
    }
    return render(request, 'event/issue_detail.html', context=ctx)


@login_required
@csrf_exempt
def delete_comment(request, pk):
    req = json.loads(request.body)
    challenge_id = req['challenge_id']
    challengeReply_id = req['challengeReply_id']

    comment = ChallengeReply.objects.get(
        challenge_id_id=challenge_id, id=challengeReply_id)
    ChallengeReply.objects.filter(
        challenge_id=challenge_id, parent_reply=comment).delete()
    comment.delete()
    commentCount = ChallengeReply.objects.filter(
        challenge_id=challenge_id).count()
    return JsonResponse({'challenge_id': challenge_id, 'challengeReply_id': challengeReply_id, 'comment_count': commentCount})


@login_required
@csrf_exempt
def delete_reply(request, pk):
    req = json.loads(request.body)
    challenge_id = req['challenge_id']
    parent_reply_id = req['parent_reply_id']
    challengeReply_id = req['challengeReply_id']
    if parent_reply_id != None:
        parent_obj = ChallengeReply.objects.get(
            challenge_id=challenge_id, id=parent_reply_id)
        ChallengeReply.objects.get(
            challenge_id=challenge_id, parent_reply=parent_obj, id=challengeReply_id).delete()
    else:
        comment = ChallengeReply.objects.get(
            challenge_id=challenge_id, id=challengeReply_id)
        ChallengeReply.objects.filter(
            challenge_id=challenge_id, parent_reply=comment).delete()
        comment.delete()
    
    commentCount = ChallengeReply.objects.filter(
        challenge_id=challenge_id).count()
    return JsonResponse({'parent_reply_id': parent_reply_id, 'challenge_id': challenge_id, 'challengeReply_id': challengeReply_id, 'comment_count':commentCount})
