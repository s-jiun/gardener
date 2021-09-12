from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    pass
