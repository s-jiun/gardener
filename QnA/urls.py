from django.urls import path
from . import views

app_name = 'QnA'

urlpatterns = [
    path('', views.qna_list, name='qnalist'),
    path('questiondetail/<int:pk>/', views.question_detail, name='questiondetail'),
    path('makequestion/', views.make_question, name='makequestion'),
    path('editquestion/<int:pk>/', views.edit_question, name='editquestion'),
    path('deletequestion/<int:pk>/', views.delete_question, name='deletequestion'),

]
