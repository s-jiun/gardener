from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TaggedPost)
class TaggedPostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
@admin.register(models.Reply)
class TaggedPostAdmin(admin.ModelAdmin):
    pass