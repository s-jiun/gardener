from django.contrib import admin
from . import models


@admin.register(models.GeneralUser)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MyPlant)
class MyPlantsAdmin(admin.ModelAdmin):
    pass
