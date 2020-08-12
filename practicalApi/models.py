from django.db import models
from django.utils import timezone

# Create your models here.


class UsersData(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="IN")


class UsersOTP(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=100)
    timestamp = models.IntegerField(default=0)
    otp=models.CharField(max_length=4)
    incorrect_attempt=models.IntegerField(default=0)
