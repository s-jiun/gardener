from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.PlantListView.as_view(), name='plant_list'),
    path('plant_detail/<int:pk>/', views.plant_detail, name="plant_detail"),
    path('scrap_ajax/', views.scrap_ajax, name='scrap_ajax'),
]
