from rest_framework import serializers
from .models import ShoppingCart
from goods.models import Course
from goods.serializers import CourseSerializer
from trade.models import OrderInfo, OrderGoods
from goods.serializers import CourseSerializer
from utils.alipay import AliPay
from store.settings import PRIVATE_KEY_PATH, ALIPAY_RETURN_URL, ALIPAY_NOTIFY_URL, ALI_PUB_KEY_PATH, DEBUG, ALI_APP_ID,ALIPAY_DEBUG_URL,ALIPAY_ONLINE_URL


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = CourseSerializer()

    class Meta:
        model = ShoppingCart
        fields = ["goods", "nums"]


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), help_text="当前用户id"
    )
    nums = serializers.IntegerField(required=True, label="商品数量", min_value=1, help_text="商品的数量，如果是线上课默认传1，后端处理报错",
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请输入购买数量",
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Course.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            if goods.online:
                raise serializers.ValidationError({
                    'num': '线上课程数目只能为1，已经添加'
                })
            else:
                existed.nums += nums
                existed.save()
        else:
            if goods.online:
                validated_data["nums"] = 1
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        if instance.goods.online:
            raise serializers.ValidationError({
                'num': '线上课程数目只能为1'
            })
        else:
            instance.nums = validated_data["nums"]
            instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = CourseSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=ALI_APP_ID,
            app_notify_url=ALIPAY_NOTIFY_URL,
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALI_PUB_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=DEBUG,  # 默认False,
            return_url=ALIPAY_RETURN_URL
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        if DEBUG:
            re_url = "{pre_url}?{data}".format(pre_url=ALIPAY_DEBUG_URL,data=url)
        else:
            re_url = "{pre_url}?{data}".format(pre_url=ALIPAY_ONLINE_URL, data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=ALI_APP_ID,
            app_notify_url=ALIPAY_NOTIFY_URL,
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALI_PUB_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=DEBUG,  # 默认False,
            return_url=ALIPAY_RETURN_URL
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    def generate_order_sn(self):
        # 当前时间+userid+随机数
        from random import Random
        import time
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
