from django.contrib import admin
from .models import ShoppingCart, OrderInfo, OrderGoods, TeacherManagement
from store.settings import ADMIN_LIST_PER_PAGE


# Register your models here.


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'nums', 'updated_datetime']
    search_fields = ('user__name', 'user__username')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_sn', 'trade_no', 'pay_status', 'order_mount', 'pay_time']
    search_fields = ['user__username', 'user__name']
    list_filter = ['pay_status']
    ordering = ['updated_datetime']
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods', 'goods_num', 'updated_datetime']
    search_fields = ['order__order_sn', 'goods__name']
    ordering = ['updated_datetime']
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class TeacherManagementAdmin(admin.ModelAdmin):
    list_display = ['user', 'commission', 'total_commission', 'scale_factor', 'updated_datetime']
    search_fields = ['user__username', 'user__name']
    ordering = ['updated_datetime']
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(TeacherManagement, TeacherManagementAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderGoods,OrderGoodsAdmin)
