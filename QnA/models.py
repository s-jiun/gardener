from django.db import models
from django.db.models.deletion import CASCADE
from account.models import GeneralUser
# Create your models here.


class CommunityQuestion(models.Model):
    user_id = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True,
                              upload_to='Question/%y/%m/%d')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
