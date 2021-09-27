from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'event'

urlpatterns = [
    path('challenge/<int:pk>/', view=views.challenge_detail,
         name='challenge_detail'),
    path('challenge/<int:pk>/delete_comment/',
         view=views.delete_comment, name='delete_comment'),
    path('challenge/<int:pk>/delete_reply/',
         view=views.delete_reply, name='delete_reply'),
    path('issue/<int:pk>/', view=views.issue_detail, name='issue_detail'),
    path('challenge/', view=views.ChallengeListView.as_view(), name='challenge'),
    path('issue/', view=views.NewsListView.as_view(), name='issue'),
    path('issue/<int:pk>/issue_delete_comment/',
         view=views.issue_delete_comment, name='issue_delete_comment'),
    path('issue/<int:pk>/issue_delete_reply/',
         view=views.issue_delete_reply, name='issue_delete_reply'),
]
