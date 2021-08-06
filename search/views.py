from django.shortcuts import render
from .models import Plant

def search_list(request):
    search_list = Plant.objects.all()
    ctx = {'search_list':  search_list }
    return render(request, 'search/search_list.html', ctx)