from django.db import models
from django.db.models.deletion import CASCADE
from user.models import GeneralUser
from taggit.managers import TaggableManager
from taggit.models import (TagBase, TaggedItemBase)
# editor
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Tag(TagBase):
    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
        max_length=100,
        allow_unicode=True,
    )


class TaggedQuestion(TaggedItemBase):
    content_object = models.ForeignKey(
        'CommunityQuestion', on_delete=models.CASCADE)
    tags = models.ForeignKey(
        'Tag', related_name='tagged_questions', on_delete=models.CASCADE, null=True)


class CommunityQuestion(models.Model):
    user_id = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(
        blank=True, null=True, config_name='answer_ckeditor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(
        verbose_name='tags', help_text='해시태그를 남겨주세요', blank=True, through=TaggedQuestion)


class CommunityAnswer(models.Model):
    user_id = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    question = models.ForeignKey(CommunityQuestion, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(
        blank=True, null=True, config_name='answer_ckeditor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
