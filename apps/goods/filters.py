from django_filters import rest_framework as filters
from .models import Course, CourseCategory
from django.db.models import Q


class CourseFilter(filters.FilterSet):
    """
    课程过滤
    """
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    top_category = filters.NumberFilter(method='top_category_filter',help_text="上级分类")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    # name = filters.CharFilter(field_name="name",lookup_expr="icontains")
    class Meta:
        model = Course
        fields = ['category', 'teacher', 'min_price', 'max_price', 'online', 'degree','top_category']


class CategoryFilter(filters.FilterSet):
    """
    类别过滤
    """

    class Meta:
        model = CourseCategory
        fields = ['category_type']
