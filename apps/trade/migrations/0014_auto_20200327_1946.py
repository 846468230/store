# Generated by Django 3.0.4 on 2020-03-27 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0013_orderinfo_marketing_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='marketing_code',
            field=models.CharField(blank=True, help_text='营销推广码', max_length=30, null=True, verbose_name='营销推广码'),
        ),
    ]
