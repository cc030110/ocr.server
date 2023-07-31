from django.db import models
from django.contrib.auth.models import AbstractUser # 장고가 제공하는 유저모델

class User(AbstractUser):
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)

    # 나만의 필드 추가
    name = models.CharField(max_length=200,default="", blank=True)
