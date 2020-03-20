from django.shortcuts import render
# Create your views here.
from .models import Course,CourseCategory
from django.views.generic.base import View
from .serializers import CourseSerializer,CourseCategorySerializer
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
from .filters import CourseFilter


class CourseCategoryListView(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
        课程分类列表数据
    retrieve:
        获取课程的分类详情
    """
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class CourseListSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CourseListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        list:
            获取课程数据
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseListSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = CourseFilter
    search_fields = ['name', 'desc', 'detail', 'tag']
    ordering_fields = ['price', 'learning_times', 'click_nums', 'added_datetime', 'degree']


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
