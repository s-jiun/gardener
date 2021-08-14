from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', view=views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', view=views.post_detail, name='post_detail'),
    path('post/create/', view=views.post_create, name='post_create'),
    path('post/<int:pk>/update/',
         view=views.post_update, name='post_update'),
    path('post/<int:pk>/delete/',
         view=views.post_delete, name='post_delete'),

    path('post/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/delete_comment/',
         views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/delete_reply/',
         views.delete_reply, name='delete_reply'),
    path('post/<int:pk>/like_ajax/', views.like_ajax, name='like_ajax'),
    path('tag/<tag>/', views.search_tag, name='search_tag'),
    path('follow_post/', views.FollowPostView.as_view(), name='follow_post_list'),
]
