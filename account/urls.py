from django.urls import path
from . import views

app_name ='account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('',views.start_page, name ="start_page"),
    path('main/', views.main_page , name= "main_page"),
]
