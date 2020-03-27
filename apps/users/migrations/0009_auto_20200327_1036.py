# Generated by Django 2.2.11 on 2020-03-27 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200327_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='id_card_back',
            field=models.ImageField(blank=True, help_text='身份证背面', null=True, upload_to='users/idcardsback/', verbose_name='身份证背面'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='id_card_front',
            field=models.ImageField(blank=True, help_text='身份证正面', null=True, upload_to='users/idcardsfront/', verbose_name='身份证正面'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='id_card_number',
            field=models.CharField(blank=True, help_text='身份证号码', max_length=20, null=True, verbose_name='身份证号码'),
        ),
    ]
