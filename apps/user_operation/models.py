from django.db import models

from django.contrib.auth import get_user_model

from goods.models import Course

# Create your models here.
User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="课程", help_text="课程id", on_delete=models.CASCADE)
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "course")

    def __str__(self):
        return self.user.name if self.user.name else self.user.username


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course = models.ForeignKey(Course, verbose_name="课程", help_text="课程id", on_delete=models.CASCADE)
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name='评论')
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course.name


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
                                       help_text=u"留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = models.CharField(max_length=100, default="", verbose_name="主题")
    message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = models.FileField(upload_to="message/images/", verbose_name="上传的文件", help_text="上传的文件")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserMessage(models.Model):
    # 如果 为 0 代表全局消息，否则就是用户的 ID
    user = models.IntegerField(default=0, verbose_name='接受用户')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class UserCourse(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户学习过的课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username + self.course.name


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    province = models.CharField(max_length=100, default="", verbose_name="省份")
    city = models.CharField(max_length=100, default="", verbose_name="城市")
    district = models.CharField(max_length=100, default="", verbose_name="区域")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    signer_name = models.CharField(max_length=100, default="", verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
