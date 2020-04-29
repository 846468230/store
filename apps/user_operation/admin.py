from django.contrib import admin
from .models import UserFav, UserAsk, CourseComments, UserLeavingMessage, UserMessage, UserCourse, UserAddress,UserCashWithdrawal
# Register your models here.
from store.settings import ADMIN_LIST_PER_PAGE
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
class UserCashWithdrawResource(resources.ModelResource):
    username = Field(attribute="user__username",column_name="用户名")
    name = Field(attribute="user__name",column_name="中文名")
    apply_category = Field(attribute="apply_category", column_name="申请种类")
    apply_status = Field(attribute="apply_status", column_name="申请状态")
    withdraw_status = Field(attribute="withdraw_status", column_name="取现状态")
    amount = Field(attribute="amount", column_name="金额")
    added_datetime = Field(attribute="added_datetime", column_name="创建时间")
    updated_datetime = Field(attribute="updated_datetime", column_name="更新时间")
    class Meta:
        model = UserCashWithdrawal
        fields = ['id','username','name','apply_category','apply_status','withdraw_status','amount','added_datetime','updated_datetime']
        export_order = ['id','username','name','apply_category','apply_status','withdraw_status','amount','added_datetime','updated_datetime']

class UserFavAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'updated_datetime']
    search_fields = ('user__name', 'user__username', 'course__name')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class UserAskAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'course', 'updated_datetime']
    search_fields = ('course__name',)
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class CourseCommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'updated_datetime']
    search_fields = ('user__name', 'user__username', 'course__name')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class UserLeavingMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_type', 'subject', 'updated_datetime']
    search_fields = ('user__name', 'user__username', 'subject', 'message')
    list_filter = ['message_type', ]
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'has_read', 'updated_datetime']
    search_fields = ('user__name', 'user__username', 'message')
    list_filter = ('has_read',)
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'updated_datetime']
    search_fields = ('user__name', 'user__username', 'course__name')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class UserCashWithdrawAdmin(ImportExportModelAdmin):
    list_display = ['user', 'apply_category','amount', 'apply_status','updated_datetime']
    search_fields = ('user__name', 'user__username')
    list_filter = ['apply_category','apply_status']
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'
    resource_class = UserCashWithdrawResource

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'province', 'city', 'district', 'updated_datetime']
    search_fields = ('user__name', 'user__username')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


admin.site.register(UserFav, UserFavAdmin)
admin.site.register(UserAsk, UserAskAdmin)
admin.site.register(CourseComments, CourseCommentsAdmin)
admin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(UserCashWithdrawal,UserCashWithdrawAdmin)
