# Generated by Django 2.2.11 on 2020-03-27 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200326_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='id_card_back',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='id_card_front',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='id_card_number',
        ),
    ]
