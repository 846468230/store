from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名",help_text="用户姓名")
    nickname = models.CharField(max_length=30,null=True,blank=True,verbose_name="昵称",help_text="用户昵称")
    avatar = models.ImageField(null=True,blank=True,upload_to='users/avatar/', verbose_name='头像', max_length=100,help_text="用户头像")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月",help_text="用户生日，日期类型")
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")), default="female",
                              verbose_name="性别",help_text="用户性别 male female")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话",help_text="电话号码 最大11位")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    session_key = models.CharField(null=True,blank=True,max_length=30,verbose_name="微信session_key",help_text="微信的session_key")
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
    code = models.CharField(max_length=10, verbose_name="验证码",help_text="短信验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话",help_text="电话号码")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间',help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间',help_text="更新时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
