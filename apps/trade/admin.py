from django.contrib import admin
from .models import ShoppingCart, OrderInfo, OrderGoods, TeacherManagement
from store.settings import ADMIN_LIST_PER_PAGE
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from marketing.models import MarketingRelationship
User = get_user_model()


# Register your models here.
class TeacherManagementResource(resources.ModelResource):
    username = Field(attribute="user__username", column_name="用户名")
    name = Field(attribute="user__name", column_name="中文名")
    commission = Field(attribute="commission", column_name="当前佣金余额")
    total_commission = Field(attribute="total_commission", column_name="当前总佣金")
    scale_factor = Field(attribute="scale_factor", column_name="佣金配置")
    added_datetime = Field(attribute="added_datetime", column_name="创建时间")
    updated_datetime = Field(attribute="updated_datetime", column_name="更新时间")

    class Meta:
        model = TeacherManagement
        fields = ['id', 'username', 'name', 'commission', 'total_commission', 'scale_factor', 'added_datetime',
                  'updated_datetime']
        export_order = ['id', 'username', 'name', 'commission', 'total_commission', 'scale_factor', 'added_datetime',
                        'updated_datetime']


class OrderInfoResource(resources.ModelResource):
    username = Field(attribute="user__username", column_name="用户名")
    name = Field(attribute="user__name", column_name="中文名")
    order_sn = Field(attribute="order_sn", column_name="订单号")
    trade_no = Field(attribute="trade_no", column_name="交易号")
    pay_status = Field(attribute="pay_status", column_name="支付状态")
    post_script = Field(attribute="post_script", column_name="留言")
    order_mount = Field(attribute="order_mount", column_name="订单金额")
    marketing_code = Field(attribute="marketing_code", column_name="推广码")
    pay_time = Field(attribute="pay_time", column_name="支付时间")
    address = Field(attribute="address", column_name="收获地址")
    signer_name = Field(attribute="signer_name", column_name="签收人")
    signer_mobile = Field(attribute="signer_mobile", column_name="签收人电话")
    added_datetime = Field(attribute="added_datetime", column_name="创建时间")
    updated_datetime = Field(attribute="updated_datetime", column_name="更新时间")

    class Meta:
        model = OrderInfo
        fields = ['id', 'username', 'name', 'order_sn', 'trade_no', 'pay_status', 'post_script',
                  'order_mount', 'marketing_code', 'pay_time', 'address', 'signer_name', 'signer_mobile',
                  'added_datetime', 'updated_datetime']
        export_order = ['id', 'username', 'name', 'order_sn', 'trade_no', 'pay_status', 'post_script',
                        'order_mount', 'marketing_code', 'pay_time', 'address', 'signer_name', 'signer_mobile',
                        'added_datetime', 'updated_datetime']


class OrderGoodsResource(resources.ModelResource):
    order_sn = Field(attribute="order__order_sn", column_name="订单号")
    trade_no = Field(attribute="order__order__trade_no", column_name="交易号")
    pay_status = Field(attribute="order__pay_status", column_name="支付状态")
    goods_id = Field(attribute="goods__id", column_name="商品id")
    goods_name = Field(attribute="goods__name", column_name="商品名")
    goods_num = Field(attribute="goods_num", column_name="商品数量")
    added_datetime = Field(attribute="added_datetime", column_name="创建时间")
    updated_datetime = Field(attribute="updated_datetime", column_name="更新时间")

    class Meta:
        model = OrderGoods
        fields = ['id', 'order_sn', 'trade_no', 'order_sn', 'pay_status', 'goods_id', 'goods_name',
                  'goods_num', 'added_datetime', 'updated_datetime']
        export_order = ['id', 'order_sn', 'trade_no', 'order_sn', 'pay_status', 'goods_id', 'goods_name',
                        'goods_num', 'added_datetime', 'updated_datetime']


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'nums', 'updated_datetime']
    search_fields = ('user__name', 'user__username')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'

class OrderInfoListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('课程代表')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'marketer'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        group = Group.objects.get(name="marketer")
        users = group.user_set.all()
        choices = [(user.id, _('%s' % (user.username,))) for user in users]
        return choices

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            users = MarketingRelationship.objects.filter(parent_marketer__id=self.value()).values('user')
            return queryset.filter(user__id__in=users)
        return queryset

class OrderInfoAdmin(ImportExportModelAdmin):
    list_display = ['user', 'order_sn','marketer', 'trade_no','pay_status', 'order_mount', 'pay_time','updated_datetime']
    search_fields = ['user__username', 'user__name']
    list_filter = ['pay_status',OrderInfoListFilter]
    ordering = ['updated_datetime']
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'
    resource_class = OrderInfoResource
    def marketer(self,obj):
        return obj.user.marketer
    marketer.short_description = '课程代表'


class OrderGoodsListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('讲师')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'teacher'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        group = Group.objects.get(name="teacher")
        users = group.user_set.all()
        choices = [(user.id, _('%s' % (user.username,))) for user in users]
        return choices

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
           return queryset.filter(goods__teacher__id=self.value())
        return queryset

class OrderGoodsAdmin(ImportExportModelAdmin):

    list_display = ['name','order', 'goods', 'confirm', 'goods_num','id_card_number','updated_datetime']
    list_filter = ['confirm',OrderGoodsListFilter]
    search_fields = ['order__order_sn', 'goods__name', "order__user__username", "order__user__name"]
    ordering = ['updated_datetime']
    list_display_links = ('name',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'
    resource_class = OrderGoodsResource


class TeacherManagementAdmin(ImportExportModelAdmin):
    list_display = ['user', 'commission', 'total_commission', 'scale_factor', 'updated_datetime']
    search_fields = ['user__username', 'user__name']
    ordering = ['updated_datetime']
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'
    resource_class = TeacherManagementResource


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(TeacherManagement, TeacherManagementAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderGoods, OrderGoodsAdmin)
