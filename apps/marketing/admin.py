from django.contrib import admin
from django import forms
from .models import MarketingRelationship
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from store.settings import ADMIN_LIST_PER_PAGE
from .models import MarketingRelationship, Poster, TeacherApplication, MarketerApplication, MarketerConfigs, \
    MarketingCode
from .forms import MarketingCodeForm
from django.contrib.auth.models import Group
# Register your models here.

from django.contrib.auth import get_user_model

User = get_user_model()


class MarketerConfigsAdmin(admin.ModelAdmin):
    list_display = ['level', 'factor_first']


class MarketingRelationshipResource(resources.ModelResource):
    username = Field(attribute="user__username", column_name="用户名")
    name = Field(attribute="user__name", column_name="中文名")
    commission = Field(attribute="commission", column_name="当前佣金余额")
    total_commission = Field(attribute="total_commission", column_name="当前总佣金")
    parent_marketer__name = Field(attribute="parent_marketer__name", column_name="课程代表")
    config = Field(attribute="config", column_name="佣金配置")
    is_freeze = Field(attribute="is_freeze", column_name="是否冻结")
    added_datetime = Field(attribute="added_datetime", column_name="创建时间")
    updated_datetime = Field(attribute="updated_datetime", column_name="更新时间")

    class Meta:
        model = MarketingRelationship
        fields = ['id', 'username', 'name', 'commission', 'total_commission', 'parent_marketer__name', 'config',
                  'is_freeze', 'added_datetime', 'updated_datetime']
        export_order = ['id', 'username', 'name', 'commission', 'total_commission', 'parent_marketer__name', 'config',
                        'is_freeze', 'added_datetime', 'updated_datetime']


class MarketingRelationshipAdmin(ImportExportModelAdmin):
    list_display = ['user', 'total_commission', 'commission', 'parent_marketer', 'config', 'is_freeze',
                    'updated_datetime']
    list_filter = ("config", "is_freeze")
    search_fields = ('user__name', 'user__username', 'parent_marketer__name', 'parent_marketer__username')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'
    resource_class = MarketingRelationshipResource

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user
        if user.groups.filter(name="market_manager").exists():
            users = MarketingRelationship.objects.all().values("user")
            queryset = queryset.filter(id__in=users)
        return queryset


class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'updated_datetime']
    search_fields = ('name', 'desc')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE


class TeacherApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'apply_status', 'updated_datetime']
    search_fields = ('user__name', 'user__username')
    list_filter = ["apply_status"]
    ordering = ('-apply_status', 'updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class MarketerApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'apply_status', 'updated_datetime']
    list_filter = ["apply_status"]
    search_fields = ('user__name', 'user__username')
    ordering = ('-apply_status', 'updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class MarketingCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'updated_datetime']
    search_fields = ('user__name', 'user__username')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'
    form = MarketingCodeForm


admin.site.register(MarketerConfigs, MarketerConfigsAdmin)
admin.site.register(MarketingRelationship, MarketingRelationshipAdmin)
admin.site.register(TeacherApplication, TeacherApplicationAdmin)
admin.site.register(Poster, PostAdmin)
admin.site.register(MarketerApplication, MarketerApplicationAdmin)
admin.site.register(MarketingCode, MarketingCodeAdmin)
