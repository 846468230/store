# Generated by Django 3.0.4 on 2020-04-25 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketing', '0007_auto_20200405_1952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='marketerapplication',
            options={'verbose_name': '课程代表申请', 'verbose_name_plural': '课程代表申请'},
        ),
        migrations.AlterModelOptions(
            name='marketerconfigs',
            options={'verbose_name': '课程代表佣金配置', 'verbose_name_plural': '课程代表佣金配置'},
        ),
        migrations.AlterModelOptions(
            name='marketingcode',
            options={'verbose_name': '课程推广码', 'verbose_name_plural': '课程推广码'},
        ),
        migrations.AlterModelOptions(
            name='marketingrelationship',
            options={'verbose_name': '服务关系', 'verbose_name_plural': '服务关系'},
        ),
        migrations.RemoveField(
            model_name='marketerconfigs',
            name='factor_second',
        ),
        migrations.AlterField(
            model_name='marketerapplication',
            name='user',
            field=models.ForeignKey(help_text='用户id', on_delete=django.db.models.deletion.CASCADE, related_name='application_marketer', to=settings.AUTH_USER_MODEL, verbose_name='申请用户'),
        ),
        migrations.AlterField(
            model_name='marketerconfigs',
            name='factor_first',
            field=models.FloatField(default=0.0, verbose_name='佣金系数'),
        ),
        migrations.AlterField(
            model_name='marketerconfigs',
            name='level',
            field=models.IntegerField(choices=[(1, '分销等级一'), (2, '分销等级二'), (3, '分销等级三')], default=1, help_text='配置等级', unique=True, verbose_name='配置等级'),
        ),
        migrations.AlterField(
            model_name='marketingcode',
            name='code',
            field=models.CharField(blank=True, help_text='推广码', max_length=30, null=True, unique=True, verbose_name='推广码'),
        ),
        migrations.AlterField(
            model_name='marketingrelationship',
            name='commission',
            field=models.FloatField(default=0.0, help_text='用户佣金', verbose_name='用户佣金'),
        ),
        migrations.AlterField(
            model_name='marketingrelationship',
            name='parent_marketer',
            field=models.ForeignKey(blank=True, help_text='课程代表', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_marketer', to=settings.AUTH_USER_MODEL, verbose_name='课程代表'),
        ),
        migrations.AlterField(
            model_name='marketingrelationship',
            name='total_commission',
            field=models.FloatField(default=0.0, help_text='历史总佣金', verbose_name='历史总佣金'),
        ),
    ]
