from rest_framework import serializers
from .models import Course, CourseCategory, Banner, Lesson, Video  # , LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth import get_user_model

User = get_user_model()


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Video


class VideoIdSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Video


class LessonDetailSerializer(serializers.ModelSerializer):
    video = VideoIdSerializer(many=True)
    class Meta:
        model = Lesson
        fields = "__all__"
class LessonSerializer(serializers.ModelSerializer):
    #video = VideoIdSerializer(many=True)
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseCategorySerializer1(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "username"]


class CourseLessonSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer1()
    teacher = TeacherSerializer(help_text="老师id")
    lesson = LessonSerializer(many=True)
    class Meta:
        model = Course
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer1()
    teacher = TeacherSerializer(help_text="老师id")

    class Meta:
        model = Course
        fields = "__all__"  # ['id','name','desc','teacher','detail','price','degree','learn_times',
        # 'students','fav_nums','image','click_nums','category','online','tag','you_need_know','teacher_tell','added_datetime','updated_datetime']


class CourseCategoryDetailSerializer1(serializers.ModelSerializer):
    goods = CourseSerializer(many=True, help_text="课程")

    class Meta:
        model = CourseCategory
        fields = "__all__"


class CourseCategoryDetailSerializer(serializers.ModelSerializer):
    sub_cat = CourseCategoryDetailSerializer1(many=True)

    class Meta:
        model = CourseCategory
        fields = "__all__"  # ['id','name','desc','teacher','detail','price','degree','learn_times',
        # 'students','fav_nums','image','click_nums','category','online','tag','you_need_know','teacher_tell','added_datetime','updated_datetime']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class CourseCategorySerializer(serializers.ModelSerializer):
    sub_cat = CourseCategorySerializer1(many=True)

    class Meta:
        model = CourseCategory
        fields = "__all__"


class CourseFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'teacher', 'price', 'degree', 'learn_times', 'image', 'online']


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
