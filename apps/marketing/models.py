from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class MarketerConfigs(models.Model):
    """
    分销系数配置
    """
    LEVEL = (
        (1, "分销等级一"),
        (2, "分销等级二"),
        (3,"分销等级三")
    )
    level = models.IntegerField(choices=LEVEL,default=LEVEL[0][0],verbose_name="分销等级", help_text="分销等级",unique=True)
    factor_first = models.FloatField(default=0.0, verbose_name="一级分销系数")
    factor_second = models.FloatField(default=0.0, verbose_name="二级分销系数")

    class Meta:
        verbose_name = "分销系数配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.level)


class MarketingRelationship(models.Model):
    user = models.OneToOneField(User,blank=True,null=True, verbose_name="用户", on_delete=models.SET_NULL, help_text="用户id",
                             related_name="user_marketer")
    commission = models.FloatField(default=0.0, verbose_name="营销佣金", help_text="营销佣金")
    parent_marketer = models.ForeignKey(User, null=True, blank=True, verbose_name="营销上级", help_text="营销上级",
                                        related_name="sub_marketer", on_delete=models.SET_NULL)
    config = models.ForeignKey(MarketerConfigs, blank=True, null=True, verbose_name="佣金配置", help_text="佣金配置",
                               on_delete=models.SET_NULL)
    is_freeze = models.BooleanField(default=False, verbose_name="是否冻结", help_text="是否冻结")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = "营销关系"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.user.username,)


class Poster(models.Model):
    name = models.CharField(max_length=52, verbose_name='海报名称', help_text="海报名称")
    desc = models.TextField(default="", verbose_name="文字描述", help_text="文字描述")
    image = models.ImageField(upload_to='marketing/images/', verbose_name='海报图', max_length=100, help_text="海报图")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = "营销海报"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TeacherApplication(models.Model):
    APPLICATION_STATUS = (
        ("SUCCESS", "申请成功"),
        ("REJECT", "申请拒绝"),
        ("APPLYING", "申请中"),
    )
    user = models.ForeignKey(User, verbose_name="申请用户", on_delete=models.CASCADE, help_text="用户id",
                             related_name="application_teaccher")
    apply_status = models.CharField(choices=APPLICATION_STATUS, default="APPLYING", max_length=30, verbose_name="申请状态",
                                    help_text="申请状态")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = "导师申请"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class MarketerApplication(models.Model):
    APPLICATION_STATUS = (
        ("SUCCESS", "申请成功"),
        ("REJECT", "申请拒绝"),
        ("APPLYING", "申请中"),
    )
    user = models.ForeignKey(User, verbose_name="申请营销", on_delete=models.CASCADE, help_text="用户id",
                             related_name="application_marketer")
    apply_status = models.CharField(choices=APPLICATION_STATUS, default="APPLYING", max_length=30, verbose_name="申请状态",
                                    help_text="申请状态")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = "营销人员申请"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class MarketingCode(models.Model):
    """
    营销推广码
    """
    user = models.ForeignKey(User, verbose_name="推广码属主", on_delete=models.CASCADE, help_text="推广码属主",
                             related_name="markceting_code")
    code = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="营销码", help_text="营销码")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = "营销推广码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user) + ""+ self.code
