from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.PlantListView.as_view(), name='plant_list'),
    path('scrap_ajax/', views.scrap_ajax, name='scrap_ajax'),
    path('plant_wiki/', views.plant_wiki, name = "plant_wiki"),
    path('edit_plant_wiki/<int:pk>',views.edit_plant_wiki, name="edit_plant_wiki"),
    path('delete_plant_wiki/<int:pk>',views.delete_plant_wiki, name="delete_plant_wiki")
]
