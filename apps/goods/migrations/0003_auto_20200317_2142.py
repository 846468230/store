# Generated by Django 3.0.4 on 2020-03-17 21:42

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20200317_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=300, verbose_name='课程描述'),
        ),
    ]
