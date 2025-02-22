from django.db import models

from django.contrib.auth import get_user_model

from goods.models import Course

# Create your models here.
User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE, help_text="用户id")
    course = models.ForeignKey(Course, verbose_name="课程", help_text="课程id", on_delete=models.CASCADE)
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "course")

    def __str__(self):
        return str(self.user)


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名', help_text="用户姓名")
    mobile = models.CharField(max_length=11, verbose_name='手机', help_text="用户手机")
    course = models.ForeignKey(Course, verbose_name="课程", help_text="课程id", on_delete=models.CASCADE)
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name + " " +self.course.name

class CourseComments(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE, help_text="用户id")
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE, help_text="课程id")
    comments = models.CharField(max_length=200, verbose_name='评论', help_text="评论内容")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user) + " "+str(self.course)


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
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE, help_text="用户id")
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
                                       help_text=u"留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = models.CharField(max_length=100, default="", verbose_name="主题", help_text="留言主题")
    message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = models.FileField(null=True, blank=True,upload_to="message/images/", verbose_name="上传的文件", help_text="上传的文件")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user) +" " +self.subject

class UserCashWithdrawal(models.Model):
    """
        用户取现
    """
    WITHDRWAL_CHOICES = (
        (1, "课程代表佣金取现"),
        (2, "教师佣金取现"),
    )
    APPLICATION_STATUS = (
        ("SUCCESS", "申请成功"),
        ("REJECT", "申请拒绝"),
        ("APPLYING", "申请中"),
    )
    WITHDRAW_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待付款"),
    )
    user = models.ForeignKey(User, verbose_name="申请用户", on_delete=models.CASCADE, help_text="用户id",
                             related_name="application_user")
    apply_category = models.IntegerField(choices=WITHDRWAL_CHOICES,verbose_name="取现类型",help_text="取现类型")
    apply_status = models.CharField(choices=APPLICATION_STATUS, default="APPLYING", max_length=30, verbose_name="申请状态",
                                    help_text="申请状态")
    withdraw_status = models.CharField(choices=WITHDRAW_STATUS, default="paying", max_length=30, verbose_name="提取状态",
                     help_text="提取状态")
    amount = models.FloatField(default=0.0,verbose_name="取现金额",help_text="取现金额")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = "取现申请"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)

class UserMessage(models.Model):
    # 如果 为 0 代表全局消息，否则就是用户的 ID
    user = models.IntegerField(default=0, verbose_name='接受用户', help_text="发给用户的id，0为全部，否则为用户id")
    message = models.CharField(max_length=500, verbose_name='消息内容', help_text="消息内容")
    has_read = models.BooleanField(default=False, verbose_name='是否已读', help_text="是否已读")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)


class UserCourse(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE, help_text="用户id")
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE, help_text="用户课程",
                               related_name="user_course")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = '用户的课程'
        verbose_name_plural = verbose_name
        unique_together = ("user", "course")

    def __str__(self):
        return str(self.user) + " " + self.course.name


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE, help_text="用户id")
    is_default = models.BooleanField(default=False, verbose_name="是否默认地址",help_text="是否默认地址")
    province = models.CharField(max_length=100, default="", verbose_name="省份", help_text="省份")
    city = models.CharField(max_length=100, default="", verbose_name="城市", help_text="城市")
    district = models.CharField(max_length=100, default="", verbose_name="区域", help_text="区域")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址", help_text="详细地址")
    signer_name = models.CharField(max_length=100, default="", verbose_name="签收人", help_text="签收人名称")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话", help_text="签收人电话")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)+ " " +self.address
