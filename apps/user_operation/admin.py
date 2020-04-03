from django.contrib import admin
from .models import UserFav, UserAsk, CourseComments, UserLeavingMessage, UserMessage, UserCourse, UserAddress,UserCashWithdrawal
# Register your models here.
from store.settings import ADMIN_LIST_PER_PAGE


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


class UserCashWithdrawAdmin(admin.ModelAdmin):
    list_display = ['user', 'apply_category', 'apply_status','amount','updated_datetime']
    search_fields = ('user__name', 'user__username')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


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
