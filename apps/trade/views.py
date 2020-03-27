from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods,TeacherManagement
from .serializers import OrderSerializer, OrderDetailSerializer,TeacherManagementSerializer
from rest_framework import mixins, viewsets
from django.shortcuts import redirect
from rest_framework.routers import reverse

# Create your views here.
class TeacherManagementViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
        订单管理
        list:
            获取教师佣金
        retrieve:
            获取教师佣金
        """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = TeacherManagementSerializer
    def get_queryset(self):
        return TeacherManagement.objects.filter(user=self.request.user)

class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order


class ShoppingCartViewSet(ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物车记录
    """
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


from rest_framework.views import APIView
from utils.alipay import AliPay
from store.settings import ALI_PUB_KEY_PATH, PRIVATE_KEY_PATH, ALIPAY_NOTIFY_URL, ALIPAY_RETURN_URL, DEBUG, ALI_APP_ID
from rest_framework.response import Response
from datetime import datetime


class AlipayView(APIView):
    def get(self, request, format=None):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid=ALI_APP_ID,
            app_notify_url=ALIPAY_NOTIFY_URL,
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALI_PUB_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=DEBUG,  # 默认False,
            return_url=ALIPAY_RETURN_URL
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            if trade_status != None:
                for existed_order in existed_orders:
                    existed_order.pay_status = trade_status
                    existed_order.trade_no = trade_no
                    existed_order.pay_time = datetime.now()
                    existed_order.save()

            response = redirect(reverse("order-list",request=request))
            return response
        else:
            response = redirect(reverse("order-list",request=request))
            return response

    def post(self, request, format=None):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid=ALI_APP_ID,
            app_notify_url=ALIPAY_NOTIFY_URL,
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALI_PUB_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=DEBUG,  # 默认False,
            return_url=ALIPAY_RETURN_URL
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")
