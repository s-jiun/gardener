from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.GeneralUser)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    pass
