# Generated by Django 3.0.4 on 2020-04-27 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0011_auto_20200427_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(default='www.baidu.com', help_text='视频地址', verbose_name='访问地址'),
        ),
    ]
