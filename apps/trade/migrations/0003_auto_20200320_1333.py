# Generated by Django 3.0.4 on 2020-03-20 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0006_auto_20200320_1333'),
        ('trade', '0002_auto_20200317_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='added_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='address',
            field=models.CharField(default='', help_text='收货地址', max_length=100, verbose_name='收货地址'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order_mount',
            field=models.FloatField(default=0.0, help_text='订单金额', verbose_name='订单金额'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order_sn',
            field=models.CharField(blank=True, help_text='订单号码', max_length=30, null=True, unique=True, verbose_name='订单号'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('TRADE_SUCCESS', '成功'), ('TRADE_CLOSED', '超时关闭'), ('WAIT_BUYER_PAY', '交易创建'), ('TRADE_FINISHED', '交易结束'), ('paying', '待支付')], default='paying', help_text='订单状态', max_length=30, verbose_name='订单状态'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_time',
            field=models.DateTimeField(blank=True, help_text='支付时间', null=True, verbose_name='支付时间'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='post_script',
            field=models.CharField(help_text='订单留言', max_length=200, verbose_name='订单留言'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='signer_name',
            field=models.CharField(default='', help_text='签收人名称', max_length=20, verbose_name='签收人'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='singer_mobile',
            field=models.CharField(help_text='签收人联系电话', max_length=11, verbose_name='联系电话'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='trade_no',
            field=models.CharField(blank=True, help_text='交易号码', max_length=100, null=True, unique=True, verbose_name='交易号'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='user',
            field=models.ForeignKey(help_text='用户id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='added_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='增加时间'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='goods',
            field=models.ForeignKey(help_text='课程id', on_delete=django.db.models.deletion.CASCADE, to='goods.Course', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='nums',
            field=models.IntegerField(default=0, help_text='购买数量默认设置为1', verbose_name='购买数量'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='updated_datetime',
            field=models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(help_text='用户id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
