from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.urls import path
from . import views
app_name = 'user'

urlpatterns = [
     path('login/', views.login, name='login'),
     path('logout/', views.logout, name='logout'),
     path('signup/', views.signup, name='signup'),
     path('signout/', views.member_del, name='signout'),
     path('update/', views.member_modification, name='update'),
     path('profile/<int:pk>', views.profile, name='profile'),
     path('profile/<int:pk>/follow', views.follow_list, name='follow'),
     path('profile/update', views.profile_update, name='profile_update'),
     path('myprofile', views.my_profile, name='my_profile'),
     path('', views.start_page, name="start_page"),
     path('following_ajax/', views.following_ajax, name='following_ajax'),
     path('follow_ajax/', views.follow_ajax, name='follow_ajax'),
     path('find_id/', views.find_id, name='find_id'),
     path('profile/<int:pk>/my_pick',
          views.liked_post_ListView.as_view(), name='my_pick'),
     path('profile/<int:pk>/my_scrab_plant',
          view=views.ScrabListView.as_view(), name='my_scrab_plant'),
     path('profile/delete_scrab/<int:pk>',
          view=views.delete_scrab, name='delete_scrab'),
     path('accounts/login/', views.login, name='account_login'),
     path('search_gardener/', login_required(views.GardenerListView.as_view()), name='search_gardener'),
     path('base_image_ajax/', views.base_image_ajax, name='base_image_ajax'),
]
