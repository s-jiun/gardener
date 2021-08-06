from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', view=views.post_list, name='post_list'),
    path('post/<int:pk>/', view=views.post_detail, name='post_detail'),
    path('post/create/', view=views.post_create, name='post_create'),
    path('post/<int:pk>/update/',
         view=views.post_update, name='post_update'),
    path('post/<int:pk>/delete/',
         view=views.post_delete, name='post_delete'),

    path('post/<int:pk>/comment_ajax/', views.add_comment, name='comment_ajax'),
]
