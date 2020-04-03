from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework import viewsets
# Create your views here.
from .serializers import UserFavSerializer, UserFavListSerializer
from .models import UserFav
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from utils.permissions import IsOwnerOrReadOnly,teacherOrmarketerAndEnough
from rest_framework.permissions import IsAuthenticated
from .serializers import UserLeavingMessageSerializer, UserAddressSerializer, UserCourseListSerializer,UserCashWithdrawSerializer
from .models import UserLeavingMessage, UserAddress, UserCourse,UserCashWithdrawal
from goods.serializers import CourseSerializer
from goods.models import Course
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

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


class UserCourseViewSet(ListModelMixin, viewsets.GenericViewSet):
    """
    用户购买的课程
    """
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Course.objects.filter(id__in = UserCourse.objects.filter(user=self.request.user).values('course'))


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
        # self.check_object_permissions(self.request, self.request.user)
        return UserFav.objects.filter(user=self.request.user)

class UserCashWithDrawViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        展示用户提取现金的申请
    create:
        展示用户具体的体现申请
    retrieve:
        展示具体的一份提取现金申请
    """
    serializer_class = UserCashWithdrawSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        apply_status = UserCashWithdrawal.APPLICATION_STATUS[2][0]
        apply_category = serializer.validated_data['apply_category']
        if UserCashWithdrawal.objects.filter(user=user, apply_status=apply_status,apply_category=apply_category).exists():
            headers = self.get_success_headers(serializer.data)
            return Response({
                "detail": "您的申请正在审核中，请勿重复申请!"
            }, status=status.HTTP_406_NOT_ACCEPTABLE, headers=headers)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return UserCashWithdrawal.objects.filter(user=self.request.user)