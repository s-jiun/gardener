from django.db.models.fields.files import ImageField
from django.shortcuts import render, get_object_or_404, redirect
from .models import CommunityAnswer, CommunityQuestion,Tag
from .forms import QuestionForm, AnswerForm
from account.models import GeneralUser
from django.views.generic import ListView


from taggit.managers import TaggableManager

def qna_list(request):
    question_list = CommunityQuestion.objects.all()
    ctx = {'question_list': question_list}
    return render(request, 'QnA/qnalist.html', ctx)


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


# def make_question(request, question=None):
#     if request.method == "POST":
#         form = QuestionForm(request.POST, request.FILES, instance=question)
#         tag_list = request.POST['tag'].split(" ")
#         question = CommunityQuestion(
#             user_id=GeneralUser.objects.get(pk =1), #여기 나중에 로그인된 유저로바꾸면 되요!
#             title=request.POST['title'],
#             content= request.POST['content'],
#             photo = request.FILES['image'],
#         )
#         for tag in tag_list:
#                 tag =Tag(tag.strip("#"))
#                 tag.save()
#                 question.tags.add(tag)
#         question.save()
#         return redirect('QnA:questiondetail', pk=question.pk)
#     else:
#         return render(request, 'QnA/makequestion.html')


def make_question(request, question=None):
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            question = CommunityQuestion()
            question.user_id = GeneralUser.objects.get(pk=1)
            question.title = form.cleaned_data['title']
            question.content = form.cleaned_data['content']
            question.photo = form.cleaned_data['photo']
            question.tags=form.cleaned_data['tags']
            question.save()
            return redirect('QnA:questiondetail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
        ctx = {'form': form}
    return render(request, 'QnA/makequestion.html', ctx)


def edit_question(request, pk):
    question = get_object_or_404(CommunityQuestion, pk=pk)
    return make_question(request, question=question)


def delete_question(request, pk):
    question = CommunityQuestion.objects.get(pk=pk)
    question.delete()
    return redirect('QnA:qnalist')


def make_answer(request, answer=None):
    if request.method == "POST":
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            answer = form.save()
            pk = answer.question.pk

            return redirect('QnA:questiondetail', pk=pk)
    else:
        form = AnswerForm(instance=answer)
        ctx = {'form': form}
    return render(request, 'QnA/makeanswer.html', ctx)


def edit_answer(request, pk):
    answer = get_object_or_404(CommunityAnswer, pk=pk)
    return make_answer(request, question=answer)


def delete_answer(request, pk):
    answer = CommunityAnswer.objects.get(pk=pk)
    pk = answer.communityquestion.pk
    answer.delete()
    return redirect('QnA:question_detail', pk=pk)
