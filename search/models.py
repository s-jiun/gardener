from django.db import models
from user.models import GeneralUser
from django.db.models.deletion import CASCADE

# Create your models here.


class Plant(models.Model):
    name = models.CharField(blank=True, max_length=200)
    photo_url = models.TextField(blank=True, null=True)
    # 식물 사진이 없을때 기본 식물 이미지 지정이 필요할 것 같음
    growth_form = models.CharField(blank=True, max_length=200)
    care_difficulty = models.CharField(blank=True, max_length=200)
    management_level = models.CharField(blank=True, max_length=200)
    water_period_spring = models.CharField(blank=True, max_length=200)
    water_period_summer = models.CharField(blank=True, max_length=200)
    water_period_autumn = models.CharField(blank=True, max_length=200)
    water_period_winter = models.CharField(blank=True, max_length=200)
    # 물주기가 계절별로 다름. 이 부분 집고 넘어가야함.
    growth_temp = models.CharField(blank=True, null=True, max_length=200)
    sunlight = models.CharField(blank=True, null=True, max_length=200)
    humidity = models.CharField(blank=True, null=True, max_length=200)
    flower = models.CharField(blank=True, max_length=200)
    content = models.TextField(blank=True)
    # season = models.CharField(max_length=20, blank=True) >> 계절정보를 찾지 못함.


class PlantScrap(models.Model):
    user = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    plant = models.ForeignKey(Plant, on_delete=CASCADE)
