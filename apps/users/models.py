from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    session_key = models.CharField(null=True,blank=True,max_length=30,verbose_name="微信session_key")
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
