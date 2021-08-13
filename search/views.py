from django.shortcuts import render
from django.contrib import messages
from .models import Plant, PlantScrap

from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required


class PlantListView(ListView):
    model = Plant
    paginate_by = 6
    # DEFAULT : <app_label>/<model_name>_list.html
    template_name = 'search/main_plant.html'
    context_object_name = 'plant_list'  # DEFAULT : <model_name>_list

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


# @login_required
# @csrf_exempt
# def like_ajax(request, pk):
#     req = json.loads(request.body)
#     post_id = req['id']
#     post = Post.objects.get(id=post_id)
#     if(Like.objects.filter(user_id=request.user, post_id=post).count() != 0):
#         Like.objects.get(user_id=request.user, post_id=post).delete()
#     else:
#         Like.objects.create(user_id=request.user, post_id=post)
#     like_count = Like.objects.filter(post_id=post).count()
#     post.save()
#     return JsonResponse({'id': post_id, 'like_count': like_count})
