from django.shortcuts import render
# Create your views here.
from .models import Course, CourseCategory, Banner, Lesson
from django.views.generic.base import View
from .serializers import CourseSerializer, CourseCategorySerializer, CourseCategoryDetailSerializer, BannerSerializer, \
    LessonDetailSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .filters import CourseFilter, CategoryFilter,LessonFilter
from .serializers import VideoSerializer, CourseLessonSerializer, LessonSerializer
from utils.permissions import boughtOrOwnerOrAdmin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class BannerListViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        轮播的商品
    """
    serializer_class = BannerSerializer
    queryset = Banner.objects.all().order_by("index")
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class CourseCategoryListView(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    list:
        课程分类列表数据
    retrieve:
        获取课程的分类详情
    """
    queryset = CourseCategory.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = CategoryFilter
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseCategoryDetailSerializer
        else:
            return CourseCategorySerializer


class CourseListSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class LessonRetrieveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        retieve:
            获取单一章节
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Lesson.objects.all()
    # serializer_class = LessonDetailSerializer
    permission_classes = [boughtOrOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filter_class = LessonFilter
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LessonDetailSerializer
        else:
            return LessonSerializer



class CourseListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        list:
            获取课程数据
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseListSetPagination
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = CourseFilter
    search_fields = ['name', 'desc', 'detail', 'tag']
    ordering_fields = ['price', 'learning_times', 'click_nums', 'added_datetime', 'degree']

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseLessonSerializer
        else:
            return CourseSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_nums += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseListSetPagination


'''
"""
基于apiview的方法
"""
class CourseListView(APIView):
    """
    List all courses, or create a new course.
    """

    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
'''
"""
django 传统的fbv方式的view
"""
class CourseListView(View):
    def get(self, request):
        """
                通过django的view实现商品列表页
                :param request:
                :return:
                """
        json_list = []
        courses = Course.objects.all()
        # for good in goods:
        #     json_dict = {}
        #     json_dict["name"] = good.name
        #     json_dict["category"] = good.category.name
        #     json_dict["market_price"] = good.market_price
        #     json_dict["add_time"] = good.add_time
        #     json_list.append(json_dict)

        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        import json
        from django.core import serializers
        json_data = serializers.serialize('json', courses)
        json_data = json.loads(json_data)
        from django.http import HttpResponse, JsonResponse
        return JsonResponse(json_data, safe=False)
'''
