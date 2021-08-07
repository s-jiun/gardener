from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    # path('', views.search_list, name='search_list'),
    path('', views.PlantListView.as_view(), name='plant_list'),
]
