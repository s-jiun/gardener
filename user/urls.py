from django.contrib import auth
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name ='user'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.member_del, name='signout'),
    path('update/',views.member_modification, name='update'),
    path('profile/<int:pk>',views.profile, name='profile'),
    path('profile/<int:pk>/follow', views.follow_list, name='follow'),
    # path('profile/<int:pk>/following', views.following_list, name='following'),
    path('profile/update',views.profile_update, name='profile_update'),
    path('myprofile',views.my_profile, name='my_profile'),
    path('',views.start_page, name ="start_page"),
    path('main/', views.main_page , name= "main_page"),
    path('following_ajax/', views.following_ajax, name='following_ajax'),
    path('follow_ajax/', views.follow_ajax, name='follow_ajax'),

]
