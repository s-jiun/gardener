from django.shortcuts import render
from django.contrib import messages
from .models import Plant

from django.views.generic import ListView
from django.db.models import Q

class PlantListView(ListView):
    model = Plant
    paginate_by = 10
    template_name = 'search/main_plant.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'plant_list'        #DEFAULT : <model_name>_list

    def get_queryset(self):
        plant_list = Plant.objects.order_by('name') 
        return plant_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1 :
            context['q'] = search_keyword
            context['type'] = search_type

        return context

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        print(search_keyword)
        search_type = self.request.GET.get('type', '')
        plant_list = Plant.objects.order_by('name') 
    
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_plant_list = plant_list.filter(Q (name__icontains=search_keyword))
                elif search_type == 'name':
                    search_plant_list = plant_list.filter(Q (name__icontains=search_keyword))
                elif search_type =='content':
                    search_plant_list = plant_list.filter(Q (content__icontains=search_keyword))
                elif search_type =='managelevel':
                     search_plant_list = plant_list.filter(Q (management_level__icontains=search_keyword))
                return search_plant_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return plant_list

 



def main_plant(request):
    return render(request, 'search/main_plant.html')


