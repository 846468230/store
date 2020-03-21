from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class CourseCategory(models.Model):
    """
    课程类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    image = models.ImageField(upload_to='category/images/', verbose_name='分类封面图', max_length=100, help_text="分类封面图")
    icon = models.ImageField(upload_to='category/icons/', verbose_name='分类图标', max_length=100, help_text="分类图标")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat", on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间',help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间',help_text="更新时间")

    class Meta:
        verbose_name = "课程类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=52, verbose_name='课程名字',help_text="课程名字")
    desc = models.CharField(max_length=300, verbose_name='课程描述',help_text="课程的描述信息")
    teacher = models.ForeignKey(User, verbose_name='讲师', null=True, blank=True, on_delete=models.CASCADE,help_text="老师id")
    detail = RichTextUploadingField(verbose_name='课程详情',help_text="课程详情信息 是一个富文本信息")
    price = models.FloatField(default=0, verbose_name="价格",help_text="课程价格")
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, verbose_name='难度',help_text="课程的难度 cj初级 zj中级 gj高级")
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)',help_text="学习时长")
    students = models.IntegerField(default=0, verbose_name='学习人数',help_text="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数',help_text="收藏人数")
    image = models.ImageField(upload_to='goods/images/', verbose_name='封面图', max_length=100,help_text="课程封面图")
    click_nums = models.IntegerField(default=0, verbose_name='点击数',help_text="点击次数")
    category = models.ForeignKey(CourseCategory, verbose_name="课程类别", on_delete=models.CASCADE,help_text="课程类型id")
    online = models.BooleanField(default=True, verbose_name="是否线上",help_text="是否线上")
    tag = models.CharField(default='', verbose_name='课程标签', max_length=10,help_text="课程标签")
    you_need_know = models.CharField(default='', max_length=300, verbose_name='课前须知',help_text="课前须知")
    teacher_tell = models.CharField(default='', max_length=300, verbose_name='老师告诉你能学什么',help_text="老师告诉你能学什么")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间',help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间',help_text="更新时间")

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


# 章节信息
class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE,help_text="课程id")
    name = models.CharField(max_length=100, verbose_name='章节名',help_text="章节名称")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间',help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间',help_text="更新时间")

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE,help_text="章节id")
    name = models.CharField(max_length=100, verbose_name='视频名',help_text="视频名称")
    url = models.URLField(max_length=200, verbose_name='访问地址', default='www.baidu.com',help_text="视频地址")
    learn_times = models.IntegerField(default=0, verbose_name='视频时长(分钟数)',help_text="视频时长")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间',help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间',help_text="更新时间")

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE,help_text="课程id")
    name = models.CharField(max_length=100, verbose_name='课件名',help_text="课件名称")
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100,help_text="资源文件")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间',help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间',help_text="更新时间")

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Banner(models.Model):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE,help_text="轮播的课程")
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片",help_text="轮播的图片文件")
    index = models.IntegerField(default=0, verbose_name="轮播顺序",help_text="轮播的序号")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间',help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间',help_text="更新时间")

    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词",help_text="热搜关键词")
    index = models.IntegerField(default=0, verbose_name="排序",help_text="排序的次序号")
    added_datetime = models.DateTimeField(auto_now_add=True, verbose_name='增加时间',help_text="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间',help_text="更新时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
