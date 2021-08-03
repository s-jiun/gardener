from django.shortcuts import render, get_object_or_404, redirect
from .models import CommunityAnswer, CommunityQuestion
from .forms import QuestionForm, AnswerForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def qna_list(request):
    question_list = CommunityQuestion.objects.all()
    ctx = {'question_list': question_list}
    return render(request, 'QnA/qnalist.html', ctx)


def question_detail(request, pk):
    question = get_object_or_404(CommunityQuestion, pk=pk)
    answer = question.communityanswer_set.all()
    ctx = {'question': question, 'answer': answer}
    return render(request, 'QnA/questiondetail.html', ctx)


def make_question(request, question=None):
    if request.method == "POST":
        form = QuestionForm(request.POST, request.Files, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('QnA:questiondetail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
        ctx = {'form': form}
    return render(request, 'QnA/makequestion.html', form)


def edit_question(request, pk):
    question = get_object_or_404(CommunityQuestion, pk=pk)
    return make_question(request, question=question)


def delete_question(request, pk):
    question = CommunityQuestion.objects.get(pk=pk)
    question.delete()
    return redirect('QnA:qna_list')
