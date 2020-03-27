from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework import viewsets
from .models import MarketingRelationship, Poster, TeacherApplication, MarketerApplication,MarketingCode
from rest_framework import status
from rest_framework.response import Response
from .serializers import MarketingRelationshipSerializer, PosterSerializer, MarketerApplicationSerializer, \
    TeacherApplicationSerializer,MarketingCodeSerializer
from django.contrib.auth.models import Group

# Create your views here.
class MarketingRelationshipViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        展示用户的营销关系
    retrieve:
        展示单一营销关系
    """
    serializer_class = MarketingRelationshipSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return MarketingRelationship.objects.filter(user=self.request.user)


class PosterViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        展示海报列表
    retrieve:
        展示某一个海报信息
    """
    serializer_class = PosterSerializer
    permission_classes = [IsAuthenticated]
    queryset = Poster.objects.all()

class MarketingCodeViewSet(ListModelMixin,RetrieveModelMixin,viewsets.GenericViewSet,CreateModelMixin):
    """
    created:
        创建用户的一个邀请码
    list:
        展示用户的推广码
    retrieve:
        展示用户的一个具体推广码
    """
    serializer_class = MarketingCodeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    def is_marketer(user):
        return user.groups.filter(name="marketer").exists()
    def get_queryset(self):
        return MarketingCode.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not MarketingCodeViewSet.is_marketer(user) :
            headers = self.get_success_headers(serializer.data)
            return Response({
                "detail": "请先申请为营销人员，再进行推广!"
            }, status=status.HTTP_406_NOT_ACCEPTABLE, headers=headers)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TeacherApplicationViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        展示教师身份的申请
    create:
        申请成为教师
    retrieve:
        展示具体的一份教师申请
    """
    serializer_class = TeacherApplicationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        apply_status = TeacherApplication.APPLICATION_STATUS[2][0]
        if TeacherApplication.objects.filter(user=user, apply_status=apply_status).exists():
            headers = self.get_success_headers(serializer.data)
            return Response({
                "detail": "您的申请正在审核中，请勿重复申请!"
            }, status=status.HTTP_406_NOT_ACCEPTABLE, headers=headers)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return TeacherApplication.objects.filter(user=self.request.user)


class MarketerApplicationViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        展示营销身份的申请
    create:
        申请成为营销人员
    retrieve:
        展示具体的一份营销申请
    """
    serializer_class = MarketerApplicationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        apply_status = MarketerApplication.APPLICATION_STATUS[2][0]
        if MarketerApplication.objects.filter(user=user, apply_status=apply_status).exists():
            headers = self.get_success_headers(serializer.data)
            return Response({
                "detail": "您的申请正在审核中，请勿重复申请!"
            }, status=status.HTTP_406_NOT_ACCEPTABLE, headers=headers)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return MarketerApplication.objects.filter(user=self.request.user)
