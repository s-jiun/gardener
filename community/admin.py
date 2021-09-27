from django.contrib import admin
from . import models

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TaggedPost)
class TaggedPostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Reply)
class TaggedPostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass
