from rest_framework import serializers
from .models import Course, CourseCategory  # , LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth import get_user_model

User = get_user_model()


class CourseCategorySerializer2(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = "__all__"


class CourseCategorySerializer1(serializers.ModelSerializer):
    sub_cat = CourseCategorySerializer2(many=True)

    class Meta:
        model = CourseCategory
        fields = "__all__"


class CourseCategorySerializer(serializers.ModelSerializer):
    sub_cat = CourseCategorySerializer1(many=True)

    class Meta:
        model = CourseCategory
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "username"]


class CourseSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer2()
    teacher = TeacherSerializer()

    class Meta:
        model = Course
        fields = "__all__"  # ['id','name','desc','teacher','detail','price','degree','learn_times',
        # 'students','fav_nums','image','click_nums','category','online','tag','you_need_know','teacher_tell','added_datetime','updated_datetime']


"""
'''
基于serializer类的序列化方法
'''
class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=52)
    price = serializers.CharField(style={'base_template': 'textarea.html'})
    image = serializers.ImageField()
    added_datetime = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        '''
        Create and return a new `Snippet` instance, given the validated data.
        '''
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''
        Update and return an existing `Snippet` instance, given the validated data.
        '''
        instance.title = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.price)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
"""
