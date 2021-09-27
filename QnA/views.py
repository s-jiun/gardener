from django.shortcuts import render, get_object_or_404, redirect
from .models import CommunityAnswer, CommunityQuestion, Questionviews
from user.models import GeneralUser
from .forms import QuestionForm, AnswerForm
from user.models import GeneralUser
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


class QuestionListView(ListView):
    model = CommunityQuestion

    paginate_by = 10

    # DEFAULT : <app_label>/<model_name>_list.html
    template_name = 'QnA/communityquestion.html'
    context_object_name = 'communityquestion_list'  # DEFAULT : <model_name>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        communityquestion_list = CommunityQuestion.objects.order_by('-id')
        if search_keyword:
            if len(search_keyword) > 1:
                search_communityquestion_list = communityquestion_list.filter(
                    tags__name=search_keyword)
                return search_communityquestion_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return communityquestion_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
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


@login_required
def question_detail(request, pk):
    question = get_object_or_404(CommunityQuestion, pk=pk)
    answer = question.communityanswer_set.all()
    new_views = Questionviews(question=question, user=request.user)

    if not Questionviews.objects.filter(question=question).filter(user=request.user):
        new_views.save()

    question_views = Questionviews.objects.filter(question=question)
    ctx = {'question': question, 'answer': answer,
           'views': len(question_views)}
    return render(request, 'QnA/questiondetail.html', ctx)


@login_required
def make_question(request, question=None):
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.user_id = GeneralUser.objects.get(
                userid=request.user.get_username())
            question = form.save()
            return redirect('QnA:questiondetail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
        if question:
            pk = question.pk
        else:
            pk = 0

        ctx = {'form': form, 'pk': pk}
    return render(request, 'QnA/makequestion.html', ctx)


@login_required
def edit_question(request, pk):
    question = get_object_or_404(CommunityQuestion, pk=pk)
    return make_question(request, question=question)


@login_required
def delete_question(request, pk):
    question = CommunityQuestion.objects.get(pk=pk)
    question.delete()
    return redirect('QnA:communityquestion_list')


@login_required
def make_answer(request, pk, answer=None):
    if request.method == "POST":
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user_id = GeneralUser.objects.get(
                userid=request.user.get_username())
            answer.question = CommunityQuestion.objects.get(pk=pk)
            pk = answer.question.pk
            answer = form.save()
            request.user.point += 10
            print(request.user.point)
            request.user.save()
            return redirect('QnA:questiondetail', pk=pk)
    else:
        form = AnswerForm()
        ctx = {'form': form, 'pk': pk}
    return render(request, 'QnA/makeanswer.html', ctx)


@login_required
def edit_answer(request, pk):
    answer = get_object_or_404(CommunityAnswer, pk=pk)
    pk = answer.question.pk
    if request.method == "POST":
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user_id = GeneralUser.objects.get(
                userid=request.user.get_username())
            answer.question = CommunityQuestion.objects.get(pk=pk)
            pk = answer.question.pk
            answer = form.save()
            return redirect('QnA:questiondetail', pk=pk)
    else:
        form = AnswerForm(instance=answer)
        ctx = {'form': form, 'pk': pk}
    return render(request, 'QnA/makeanswer.html', ctx)


@login_required
def delete_answer(request, pk):
    answer = CommunityAnswer.objects.get(pk=pk)
    pk = answer.question.pk
    answer.delete()
    return redirect('QnA:questiondetail', pk=pk)


class TaggingListView(ListView):
    model = CommunityQuestion

    paginate_by = 10

    # DEFAULT : <app_label>/<model_name>_list.html
    template_name = 'taggit/taggit_post_list.html'
    context_object_name = 'taggedquestion_list'  # DEFAULT : <model_name>_list

    def get_queryset(self):
        search_keyword = self.kwargs['tag']
        print(search_keyword)
        question_list = CommunityQuestion.objects.order_by('-id')
        tagged_question_list = question_list.filter(tags__name=search_keyword)
        return tagged_question_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
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
        search_keyword = self.kwargs['tag']

        if len(search_keyword) > 1:
            context['tag'] = search_keyword

        return context
