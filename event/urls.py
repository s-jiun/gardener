from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'event'

urlpatterns = [
    path('challenge/<int:pk>/', view=views.challenge_detail, name='challenge_detail'),
    path('challenge/<int:pk>/delete_comment/', view=views.delete_comment, name='delete_comment'),
    path('challenge/<int:pk>/delete_reply/', view=views.delete_reply, name='delete_reply'),
    # path('challenge/create/', view=views.challenge_create, name='challenge_create'),
    # path('challenge/<int:pk>/update/',
    #      view=views.challenge_update, name='challenge_update'),
    # path('challenge/<int:pk>/delete/',
    #      view=views.challenge_delete, name='challenge_delete'),
    path('issue/<int:pk>/', view=views.issue_detail, name='issue_detail'),
    path('challenge/', view=views.ChallengeListView.as_view(), name='challenge'),
    path('issue/', view=views.NewsListView.as_view(), name='issue'),
]
