from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin,UpdateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from utils.yunpian import YunPian
from store.settings import APIKEY
from random import choice
from .models import VerifyCode
from .serializers import SmsSerializer, UserRegSerializer,UserDetailSerializer
from  django.shortcuts import get_object_or_404
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

# Create your views here.

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewSet(CreateModelMixin,UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    create:
        用户注册
    retrieve:
        用户详情
    update:
        用户更新
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsAuthenticated(),]
        elif self.action == "create":
            return []
        else:
            return []

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        else:
            return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        data_dict = serializer.data
        payload = jwt_payload_handler(user)
        data_dict["token"] = jwt_encode_handler(payload)
        data_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(data_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user)
        return self.request.user


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成六位验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        """
        重写了CreateModelMixin的creat方法
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)
