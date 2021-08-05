from django.contrib import admin
from . import models

# Register your models here.
# Photo 클래스를 inline으로 나타낸다.


class ImageInline(admin.TabularInline):
    model = models.Image


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]


@admin.register(models.TaggedPost)
class TaggedPostAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ['name','slug']

@admin.register(models.Reply)
class TaggedPostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    pass
