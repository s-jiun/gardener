from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('community/', view=views.post_list, name='post_list'),
    path('community/<int:pk>/', view=views.post_detail, name='post_detail'),
    path('community/create/', view=views.post_create, name='post_create'),
    path('community/<int:pk>/update/',
         view=views.post_update, name='post_update'),
    path('community/<int:pk>/delete/',
         view=views.post_delete, name='post_delete'),
]
