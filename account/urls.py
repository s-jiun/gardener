from django.urls import path
from . import views

app_name ='account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.member_del, name='signout'),
    path('update/',views.member_modification, name='update'),
    path('profile/<int:pk>',views.profile, name='profile'),
    path('profile/<int:pk>/follower', views.follower_list, name='follower'),
    path('profile/<int:pk>/following', views.following_list, name='following'),
    path('profile/update',views.profile_update, name='profile_update'),
    path('myprofile',views.my_profile, name='my_profile'),
    path('',views.start_page, name ="start_page"),
    path('main/', views.main_page , name= "main_page"),
]
