# Generated by Django 2.2.11 on 2020-03-27 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketing', '0004_auto_20200327_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketerConfigs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(1, '分销等级一'), (2, '分销等级二'), (3, '分销等级三')], default=1, help_text='分销等级', unique=True, verbose_name='分销等级')),
                ('factor_first', models.FloatField(default=0.0, verbose_name='一级分销系数')),
                ('factor_second', models.FloatField(default=0.0, verbose_name='二级分销系数')),
            ],
            options={
                'verbose_name_plural': '分销系数配置',
                'verbose_name': '分销系数配置',
            },
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='海报名称', max_length=52, verbose_name='海报名称')),
                ('desc', models.TextField(default='', help_text='文字描述', verbose_name='文字描述')),
                ('image', models.ImageField(help_text='海报图', upload_to='marketing/images/', verbose_name='海报图')),
                ('added_datetime', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间')),
                ('updated_datetime', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
            ],
            options={
                'verbose_name_plural': '营销海报',
                'verbose_name': '营销海报',
            },
        ),
        migrations.CreateModel(
            name='TeacherApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_status', models.CharField(choices=[('SUCCESS', '申请成功'), ('REJECT', '申请拒绝'), ('APPLYING', '申请中')], default='APPLYING', help_text='申请状态', max_length=30, verbose_name='申请状态')),
                ('added_datetime', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间')),
                ('updated_datetime', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('user', models.ForeignKey(help_text='用户id', on_delete=django.db.models.deletion.CASCADE, related_name='application_teaccher', to=settings.AUTH_USER_MODEL, verbose_name='申请用户')),
            ],
            options={
                'verbose_name_plural': '导师申请',
                'verbose_name': '导师申请',
            },
        ),
        migrations.CreateModel(
            name='MarketingRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission', models.FloatField(default=0.0, help_text='营销佣金', verbose_name='营销佣金')),
                ('is_freeze', models.BooleanField(default=False, help_text='是否冻结', verbose_name='是否冻结')),
                ('added_datetime', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间')),
                ('updated_datetime', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('config', models.ForeignKey(blank=True, help_text='佣金配置', null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing.MarketerConfigs', verbose_name='佣金配置')),
                ('parent_marketer', models.ForeignKey(blank=True, help_text='营销上级', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_marketer', to=settings.AUTH_USER_MODEL, verbose_name='营销上级')),
                ('user', models.OneToOneField(blank=True, help_text='用户id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_marketer', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name_plural': '营销关系',
                'verbose_name': '营销关系',
            },
        ),
        migrations.CreateModel(
            name='MarketingCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, help_text='营销码', max_length=30, null=True, unique=True, verbose_name='营销码')),
                ('added_datetime', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间')),
                ('updated_datetime', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('user', models.ForeignKey(help_text='推广码属主', on_delete=django.db.models.deletion.CASCADE, related_name='markceting_code', to=settings.AUTH_USER_MODEL, verbose_name='推广码属主')),
            ],
            options={
                'verbose_name_plural': '营销推广码',
                'verbose_name': '营销推广码',
            },
        ),
        migrations.CreateModel(
            name='MarketerApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_status', models.CharField(choices=[('SUCCESS', '申请成功'), ('REJECT', '申请拒绝'), ('APPLYING', '申请中')], default='APPLYING', help_text='申请状态', max_length=30, verbose_name='申请状态')),
                ('added_datetime', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间')),
                ('updated_datetime', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('user', models.ForeignKey(help_text='用户id', on_delete=django.db.models.deletion.CASCADE, related_name='application_marketer', to=settings.AUTH_USER_MODEL, verbose_name='申请营销')),
            ],
            options={
                'verbose_name_plural': '营销人员申请',
                'verbose_name': '营销人员申请',
            },
        ),
    ]
