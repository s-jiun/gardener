from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from user.models import Follow, GeneralUser
from .models import Challenge, Issue

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


def challenge_detail(request,pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    ctx={
        'challenge':challenge
    }
    return render(request,'event/challenge_detail.html', context=ctx)
   

class IssueListView(ListView):
    model = Issue
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
        issue_list = Issue.objects.order_by('-id')
        if search_keyword:
            if len(search_keyword) > 1:
                return issue_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return issue_list


def issue_detail(request,pk):
    issue = get_object_or_404(Issue, pk=pk)
    ctx={
        'issue' : issue
    }
    return render(request,'event/issue_detail.html', context=ctx)
