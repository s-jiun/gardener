from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
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
    path('other_delete_ajax/', views.other_delete_ajax, name='other_delete_ajax'),
    path('following_ajax/', views.following_ajax, name='follow_ajax'),
    path('following_delete_ajax/', views.following_delete_ajax,
         name='following_delete_ajax'),
    path('follower_delete_ajax/', views.follower_delete_ajax,
         name='follower_delete_ajax'),
    path('find_id/', views.find_id, name='find_id'),
    path('profile/<int:pk>/my_pick',
         login_required(views.liked_post_ListView.as_view()), name='my_pick'),
    path('profile/<int:pk>/my_scrab_plant',
         login_required(views.ScrabListView.as_view()), name='my_scrab_plant'),
    path('profile/<int:pk>/my_plants',
         login_required(views.MyPlantsListView.as_view()), name='my_plants'),
    path('profile/add_myplant', views.add_myplant, name='add_myplant'),
    path('profile/delete_scrab/<int:pk>',
         view=views.delete_scrab, name='delete_scrab'),
    path('accounts/login/', views.login, name='account_login'),
    path('search_gardener/', login_required(views.GardenerListView.as_view()),
         name='search_gardener'),
    path('base_image_ajax/', views.base_image_ajax, name='base_image_ajax'),
    path('save_image_ajax/', views.save_image_ajax, name='save_image_ajax'),
    path('about/', views.about, name='about'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/', views.send_mail, name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]
