# Generated by Django 3.0.4 on 2020-03-19 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='session_key',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='微信session_key'),
        ),
    ]
