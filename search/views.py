from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Plant, PlantScrap
from .forms import PlantWikiForm
from django.views.generic import ListView
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from user.models import GeneralUser

class PlantListView(ListView):
    model = Plant
    paginate_by = 6
    template_name = 'search/main_plant.html'
    context_object_name = 'plant_list'

    def get_queryset(self):
        plant_list = Plant.objects.order_by('name')
        return plant_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plants'] = Plant.objects.all()
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) /
                          page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        scrap_plant_list = []
        if self.request.user.is_authenticated:
            user = self.request.user
            scrap_list = PlantScrap.objects.filter(user=user)
            for scrap in scrap_list:
                plant = Plant.objects.get(pk=scrap.plant.pk)
                scrap_plant_list.append(plant)

        else:
            scrap_plant_list = []

        context['scrap_plant_list'] = scrap_plant_list
        if len(search_keyword) > 1:
            context['q'] = search_keyword
            context['type'] = search_type

        return context

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        plant_list = Plant.objects.order_by('name')

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_plant_list = plant_list.filter(
                        Q(name__icontains=search_keyword))
                elif search_type == 'name':
                    search_plant_list = plant_list.filter(
                        Q(name__icontains=search_keyword))
                elif search_type == 'content':
                    search_plant_list = plant_list.filter(
                        Q(content__icontains=search_keyword))
                elif search_type == 'managelevel':
                    search_plant_list = plant_list.filter(
                        Q(management_level__icontains=search_keyword))
                return search_plant_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return plant_list


def main_plant(request):
    return render(request, 'search/main_plant.html')


def plant_detail(request, pk):
    plant = Plant.objects.get(pk=pk)
    ctx = {
        "plant": plant
    }
    return render(request, "search/plant_detail.html", ctx)


@csrf_exempt
def scrap_ajax(request):
    req = json.loads(request.body)
    plant_id = req['Id']
    plant = Plant.objects.get(pk=plant_id)
    user = request.user

    if PlantScrap.objects.filter(user=user).filter(plant=plant):
        scrap = PlantScrap.objects.filter(user=user).get(plant=plant)
        scrap.delete()
        button_type = 'del_scrap'
    else:
        scrap = PlantScrap(user=user, plant=plant)
        scrap.save()
        button_type = 'scrap'
    return JsonResponse({'id': plant.pk, 'type': button_type})

@login_required
def plant_wiki(request):
    if request.method == "POST":
        form = PlantWikiForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.plant_owner = GeneralUser.objects.get(
                userid=request.user.get_username())
            plant = form.save()
            return redirect('search:plant_list')
    else:
        form = PlantWikiForm()
        ctx = {'form': form}
    return render(request, 'search/make_plant_wiki.html', ctx)


@login_required
def edit_plant_wiki(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == "POST":
        form = PlantWikiForm(request.POST, request.FILES, instance = plant)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.plant_owner = GeneralUser.objects.get(
                userid=request.user.get_username())
            plant = form.save()
            return redirect('search:plant_list')
    else:
        form = PlantWikiForm(instance=plant)
        ctx = {'form': form, 'pk': pk}
    return render(request, 'search/edit_plant_wiki.html', ctx)


@login_required
def delete_plant_wiki(request, pk):
    plant = Plant.objects.get(pk=pk)
    plant.delete()
    return redirect('search:plant_list')

    