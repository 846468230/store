# Generated by Django 3.0.4 on 2020-03-28 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0005_marketerapplication_marketerconfigs_marketingcode_marketingrelationship_poster_teacherapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketingrelationship',
            name='total_commission',
            field=models.FloatField(default=0.0, help_text='历史营销总佣金', verbose_name='历史营销总佣金'),
        ),
    ]
