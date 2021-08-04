from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.CommunityQuestion)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CommunityAnswer)
class Answerdmin(admin.ModelAdmin):
    pass
