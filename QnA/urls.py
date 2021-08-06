from django.urls import path
from . import views

app_name = 'QnA'

urlpatterns = [
    path('', views.qna_list, name='qnalist'),
    path('questiondetail/<int:pk>/', views.question_detail, name='questiondetail'),
    path('makequestion/', views.make_question, name='makequestion'),
    path('editquestion/<int:pk>/', views.edit_question, name='editquestion'),
    path('deletequestion/<int:pk>/', views.delete_question, name='deletequestion'),
    path('tag/<str:tag>', views.TaggedObjectLV.as_view(),
         name='tagged_object_list'),

    path('makeanswer/', views.make_answer, name='makeanswer'),
    path('editanswer/<int:pk>/', views.edit_answer, name='editanswer'),
    path('deleteanswer/<int:pk>/', views.delete_answer, name='deleteanswer'),

]
