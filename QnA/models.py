from django.db import models
from django.db.models.deletion import CASCADE
from user.models import GeneralUser
from taggit.managers import TaggableManager
from taggit.models import (TagBase, TaggedItemBase)
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
    photo = models.ImageField(null=True, blank=True,
                              upload_to='Question/%y/%m/%d')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(
        verbose_name='tags', help_text='A comma-separated list of tags.', blank=True, through=TaggedQuestion)


class CommunityAnswer(models.Model):
    user_id = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    question = models.ForeignKey(CommunityQuestion, on_delete=CASCADE)
    # ERD에 빠진 것 같은데 일단 필요할 것 같아서 추가해놨습니다.
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True,
                              upload_to='Answer/%y/%m/%d')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
