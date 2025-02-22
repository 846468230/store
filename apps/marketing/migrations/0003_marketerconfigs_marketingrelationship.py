# Generated by Django 3.0.4 on 2020-03-26 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketing', '0002_auto_20200326_2046'),
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
                'verbose_name': '分销系数配置',
                'verbose_name_plural': '分销系数配置',
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
                'verbose_name': '营销关系',
                'verbose_name_plural': '营销关系',
            },
        ),
    ]
