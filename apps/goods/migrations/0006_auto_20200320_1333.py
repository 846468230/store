# Generated by Django 3.0.4 on 2020-03-20 13:33

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0005_auto_20200317_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='added_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='goods',
            field=models.ForeignKey(help_text='轮播的课程', on_delete=django.db.models.deletion.CASCADE, to='goods.Course', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(help_text='轮播的图片文件', upload_to='banner', verbose_name='轮播图片'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='index',
            field=models.IntegerField(default=0, help_text='轮播的序号', verbose_name='轮播顺序'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='course',
            name='added_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间'),
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ForeignKey(help_text='课程类型id', on_delete=django.db.models.deletion.CASCADE, to='goods.CourseCategory', verbose_name='课程类别'),
        ),
        migrations.AlterField(
            model_name='course',
            name='click_nums',
            field=models.IntegerField(default=0, help_text='点击次数', verbose_name='点击数'),
        ),
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('cj', '初级'), ('zj', '中级'), ('gj', '高级')], help_text='课程的难度 cj初级 zj中级 gj高级', max_length=2, verbose_name='难度'),
        ),
        migrations.AlterField(
            model_name='course',
            name='desc',
            field=models.CharField(help_text='课程的描述信息', max_length=300, verbose_name='课程描述'),
        ),
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='课程详情信息 是一个富文本信息', verbose_name='课程详情'),
        ),
        migrations.AlterField(
            model_name='course',
            name='fav_nums',
            field=models.IntegerField(default=0, help_text='收藏人数', verbose_name='收藏人数'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(help_text='课程封面图', upload_to='goods/images/', verbose_name='封面图'),
        ),
        migrations.AlterField(
            model_name='course',
            name='learn_times',
            field=models.IntegerField(default=0, help_text='学习时长', verbose_name='学习时长(分钟数)'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(help_text='课程名字', max_length=52, verbose_name='课程名字'),
        ),
        migrations.AlterField(
            model_name='course',
            name='online',
            field=models.BooleanField(default=True, help_text='是否线上', verbose_name='是否线上'),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.FloatField(default=0, help_text='课程价格', verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.IntegerField(default=0, help_text='学习人数', verbose_name='学习人数'),
        ),
        migrations.AlterField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', help_text='课程标签', max_length=10, verbose_name='课程标签'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, help_text='老师id', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='讲师'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', help_text='老师告诉你能学什么', max_length=300, verbose_name='老师告诉你能学什么'),
        ),
        migrations.AlterField(
            model_name='course',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='course',
            name='you_need_know',
            field=models.CharField(default='', help_text='课前须知', max_length=300, verbose_name='课前须知'),
        ),
        migrations.AlterField(
            model_name='coursecategory',
            name='added_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间'),
        ),
        migrations.AlterField(
            model_name='coursecategory',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='added_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='course',
            field=models.ForeignKey(help_text='课程id', on_delete=django.db.models.deletion.CASCADE, to='goods.Course', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='download',
            field=models.FileField(help_text='资源文件', upload_to='course/resource/%Y/%m', verbose_name='资源文件'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='name',
            field=models.CharField(help_text='课件名称', max_length=100, verbose_name='课件名'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='hotsearchwords',
            name='added_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间'),
        ),
        migrations.AlterField(
            model_name='hotsearchwords',
            name='index',
            field=models.IntegerField(default=0, help_text='排序的次序号', verbose_name='排序'),
        ),
        migrations.AlterField(
            model_name='hotsearchwords',
            name='keywords',
            field=models.CharField(default='', help_text='热搜关键词', max_length=20, verbose_name='热搜词'),
        ),
        migrations.AlterField(
            model_name='hotsearchwords',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='added_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(help_text='课程id', on_delete=django.db.models.deletion.CASCADE, to='goods.Course', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(help_text='章节名称', max_length=100, verbose_name='章节名'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='video',
            name='added_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间'),
        ),
        migrations.AlterField(
            model_name='video',
            name='learn_times',
            field=models.IntegerField(default=0, help_text='视频时长', verbose_name='视频时长(分钟数)'),
        ),
        migrations.AlterField(
            model_name='video',
            name='lesson',
            field=models.ForeignKey(help_text='章节id', on_delete=django.db.models.deletion.CASCADE, to='goods.Lesson', verbose_name='章节'),
        ),
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.CharField(help_text='视频名称', max_length=100, verbose_name='视频名'),
        ),
        migrations.AlterField(
            model_name='video',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(default='www.baidu.com', help_text='视频地址', verbose_name='访问地址'),
        ),
    ]
