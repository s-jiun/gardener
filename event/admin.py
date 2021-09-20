from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.CardNews)
class CardNewsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.NewsReply)
class CardNewsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ChallengeReply)
class ChallengeReplyAdmin(admin.ModelAdmin):
    pass