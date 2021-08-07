from django.db.models.fields.files import ImageField
from django.shortcuts import render, get_object_or_404, redirect
from .models import CommunityAnswer, CommunityQuestion
from .forms import QuestionForm, AnswerForm
from account.models import GeneralUser
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from taggit.managers import TaggableManager
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


class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = CommunityQuestion

    def get_queryset(self):
        return CommunityQuestion.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context


def question_detail(request, pk):
    question = get_object_or_404(CommunityQuestion, pk=pk)
    answer = question.communityanswer_set.all()
    ctx = {'question': question, 'answer': answer}
    return render(request, 'QnA/questiondetail.html', ctx)


def make_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            # question = CommunityQuestion()
            # question.user_id = GeneralUser.objects.get(pk=1)
            # question.title = form.cleaned_data['title']
            # question.content = form.cleaned_data['content']
            # question.photo = form.cleaned_data['photo']
            # question.tags=form.cleaned_data['tags']
            # # request.POST['i']
            question = form.save(commit=False)
            question.user_id = GeneralUser.objects.get(pk=1)
            question = form.save()
            return redirect('QnA:questiondetail', pk=question.pk)
    else:
        form = QuestionForm()
        ctx = {'form': form}
    return render(request, 'QnA/makequestion.html', ctx)


@login_required
def edit_question(request, pk):
    question = get_object_or_404(CommunityQuestion, pk=pk)
    return make_question(request, question=question)


@login_required
def delete_question(request, pk):
    question = CommunityQuestion.objects.get(pk=pk)
    question.delete()
    return redirect('QnA:qnalist')


@login_required
def make_answer(request, pk, answer=None):
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
        # user_id = GeneralUser.objects.get(
        #     userid=request.user.get_username())
        # question = CommunityQuestion.objects.get(pk=pk)
        form = AnswerForm(instance=answer)
        ctx = {'form': form}
    return render(request, 'QnA/makeanswer.html', ctx)


@login_required
def edit_answer(request, pk):
    answer = get_object_or_404(CommunityAnswer, pk=pk)
    pk = answer.question.pk
    return make_answer(request, pk, answer=answer)


@login_required
def delete_answer(request, pk):
    answer = CommunityAnswer.objects.get(pk=pk)
    pk = answer.question.pk
    answer.delete()
    return redirect('QnA:questiondetail', pk=pk)
