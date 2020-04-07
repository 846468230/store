from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Course

User = get_user_model()


# Create your models here.

class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE, help_text="用户id")
    goods = models.ForeignKey(Course, verbose_name="商品", on_delete=models.CASCADE, help_text="课程id")
    buy_it = models.BooleanField(default=True, verbose_name="是否购买", help_text="是否购买")
    nums = models.IntegerField(default=0, verbose_name="购买数量", help_text="购买数量默认设置为1")

    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return str(self.user) +" " +str(self.goods)


class TeacherManagement(models.Model):
    """
    老师的佣金管理
    """
    user = models.OneToOneField(User, verbose_name="用户", on_delete=models.CASCADE, help_text="用户id",related_name="teacher_commission")
    commission = models.FloatField(default=0.0, verbose_name="佣金金额", help_text="佣金金额")
    total_commission = models.FloatField(default=0.0, verbose_name="历史总佣金", help_text="历史总佣金")
    scale_factor = models.FloatField(default=0.0,verbose_name="佣金系数", help_text="佣金系数")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = '老师佣金'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )

    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE, help_text="用户id")
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单号", help_text="订单号码")
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="交易号",
                                help_text="交易号码")
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="订单状态",
                                  help_text="订单状态")
    post_script = models.CharField(max_length=200, verbose_name="订单留言", help_text="订单留言")
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额", help_text="订单金额")
    marketing_code = models.CharField(max_length=30, null=True, blank=True, verbose_name="营销推广码", help_text="营销推广码")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间", help_text="支付时间")

    # 用户信息
    address = models.CharField(max_length=100, default="", verbose_name="收货地址", help_text="收货地址")
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人", help_text="签收人名称")
    signer_mobile = models.CharField(max_length=11, verbose_name="联系电话", help_text="签收人联系电话")

    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间', help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text="更新时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)+" "+str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单的商品详情
    """
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", related_name="ordergoods", on_delete=models.CASCADE)
    goods = models.ForeignKey(Course, verbose_name="商品", on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")

    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间')
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn) + " " + str(self.goods)
