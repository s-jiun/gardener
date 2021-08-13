from django.contrib import admin
from . import models


@admin.register(models.Plant)
class PlantAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PlantScrap)
class PlantScrapAdmin(admin.ModelAdmin):
    pass
