from django.db import models

# Create your models here.


class Plant(models.Model):
    name = models.CharField(blank=True, max_length=200)
    photo = models.ImageField(upload_to='plant', default='base/baseimg.png')
    # 식물 사진이 없을때 기본 식물 이미지 지정이 필요할 것 같음

    water_period = models.PositiveIntegerField(blank=True, null=True)
    # 물주기가 계절별로 다름. 이 부분 집고 넘어가야함.

    growth_velocity = models.PositiveIntegerField(blank=True, null=True)
    growth_type = models.TextField(blank=True)
    # 생장형은 건조 식물엔 있는데 실내 식물 자료에는 없습니다.

    sunlight = models.PositiveIntegerField(blank=True, null=True)
    growth_temp = models.PositiveIntegerField(blank=True, null=True)
    care_difficulty = models.PositiveIntegerField(blank=True, null=True)
    humidity = models.PositiveIntegerField(blank=True, null=True)
    content = models.TextField(blank=True)
    # season = models.CharField(max_length=20, blank=True) >> 계절정보를 찾지 못함.
