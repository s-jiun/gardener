from django.db import models
from django.db.models.deletion import CASCADE
from ckeditor_uploader.fields import RichTextUploadingField
from user.models import GeneralUser


# tag 관련 module import
from taggit.managers import TaggableManager
from taggit.models import (
    TagBase, TaggedItemBase
)
# TagBase를 상속받은 tag model


class Tag(TagBase):

    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
        max_length=100,
        allow_unicode=True,
    )

# Tag와 Tag가 달리는 게시물 연결하는 N:M 중개모델


class TaggedPost(TaggedItemBase):
    content_object = models.ForeignKey('Post', on_delete=models.CASCADE)
    tags = models.ForeignKey(
        'Tag', related_name='tagged_post', on_delete=models.CASCADE, null=True)


class Post(models.Model):
    user_id = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(
        default='../static/images/default_profile.svg', upload_to='Community/%y/%m/%d/')
    content = RichTextUploadingField(blank=True, null=True)
    # 태그 부분 taggit 설치  & admin 부분 확인 필요!
    tags = TaggableManager(
        verbose_name='tags', help_text='A hashtag-separated list of tags.', blank=True, through=TaggedPost)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# class Image(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     files = models.ImageField(null=True, blank=True, upload_to='Post/%y/%m/%d')


class Comments(models.Model):  # 댓글
    user_id = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    post_id = models.ForeignKey(Post, on_delete=CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reply(models.Model):  # 대댓글 까지 가능한 댓글?
    user_id = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    post_id = models.ForeignKey(Post, on_delete=CASCADE)  # 게시글 번호
    content = RichTextUploadingField(blank=True, null=True)
    parent_reply = models.ForeignKey(
        'self', on_delete=CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user_id = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    post_id = models.ForeignKey(Post, on_delete=CASCADE)
    is_like = models.BooleanField(default=True)
