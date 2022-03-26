from django.db import models
from user.models import GeneralUser
from django.db.models.deletion import CASCADE
from config import settings

import os
from uuid import uuid4
from django.utils import timezone
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete


def date_upload_to(instance, filename):
  # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
  ymd_path = timezone.now().strftime('%Y/%m/%d') 
  # 길이 32 인 uuid 값
  uuid_name = uuid4().hex
  # 확장자 추출
  extension = os.path.splitext(filename)[-1].lower()
  # 결합 후 return
  return '/'.join([
    ymd_path,
    uuid_name + extension,
  ])

# def path_file():
#     def wrapper(user, filename):
#         file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'file_upload')
#         if os.path.exists(file_upload_dir):
#             import shutil
#             shutil.rmtree(file_upload_dir)
#         return os.path.join(file_upload_dir, filename)
#     return wrapper
# # Create your models here.


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
    plant_owner = models.ForeignKey(GeneralUser, on_delete=CASCADE, null= True)
    # season = models.CharField(max_length=20, blank=True) >> 계절정보를 찾지 못함.

class Plant_register(models.Model):
    check = models.BooleanField(default = False)
    name = models.CharField(blank=True, max_length=200, verbose_name= "식물명")
    photo= models.ImageField(blank = True, null = True, upload_to= date_upload_to, verbose_name= "식물 사진")

    #성장형
    growth_form_choice = (("직립형", "직립형"), ("관목형", "관목형"), ("덩굴성", "덩굴성"), ("로제트형", "로제트형"), ("다육형", "다육형"), ("기타", "기타"))
    growth_form = models.CharField(blank=True, max_length=100, choices = growth_form_choice, verbose_name= "생장형")
    # 관리 수준
    management_level_choice = (("lv1","낮음(잘견딤)"), ("lv2", "보통(약간 돌봄)"), ("lv3", "높음(세심한 관리 필요)"))
    management_level = models.CharField(max_length= 100, choices = management_level_choice, verbose_name="관리 수준")
    # 물주기(계절별)
    water_period_spring = models.CharField(blank=True, max_length=200, verbose_name="물주기(봄)")
    water_period_summer = models.CharField(blank=True, max_length=200, verbose_name="물주기(여름)")
    water_period_autumn = models.CharField(blank=True, max_length=200, verbose_name="물주기(가을))")
    water_period_winter = models.CharField(blank=True, max_length=200, verbose_name="물주기(겨울)")

    growth_temp = models.CharField(blank=True, null=True, max_length=200, verbose_name="생장주기")
    sunlight = models.CharField(blank=True, null=True, max_length=200, verbose_name="광도")
    humidity = models.CharField(blank=True, null=True, max_length=200, verbose_name="습도")
    flower = models.CharField(blank=True, max_length=200, verbose_name="개화")
    content = models.TextField(blank=True, verbose_name="기타내용")

    plant_owner = models.ForeignKey(GeneralUser, on_delete=CASCADE)



class PlantScrap(models.Model):
    user = models.ForeignKey(GeneralUser, on_delete=CASCADE)
    plant = models.ForeignKey(Plant, on_delete=CASCADE)
