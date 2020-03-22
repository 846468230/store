from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework import viewsets
# Create your views here.
from .serializers import UserFavSerializer, UserFavListSerializer
from .models import UserFav
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .serializers import UserLeavingMessageSerializer, UserAddressSerializer
from .models import UserLeavingMessage, UserAddress


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    create:
        用户地址创建
    retrieve:
        地址详情
    update:
        地址更新
    list:
        地址列表
    Destroy:
        地址删除
    """
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class UserLeavingMessageViewSet(CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    用户留言
    """
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = UserLeavingMessageSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserFavViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户收藏
    """
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    # serializer_class = UserFavSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    lookup_field = "course_id"

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavListSerializer
        elif self.action == "create":
            return UserFavSerializer
        else:
            return UserFavListSerializer

    def get_queryset(self):
        #self.check_object_permissions(self.request, self.request.user)
        return UserFav.objects.filter(user=self.request.user)
