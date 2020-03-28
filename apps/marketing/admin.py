from django.contrib import admin
from django import forms
from .models import MarketingRelationship
from store.settings import ADMIN_LIST_PER_PAGE
from .models import MarketingRelationship,Poster,TeacherApplication,MarketerApplication,MarketerConfigs,MarketingCode
# Register your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

class MarketerConfigsAdmin(admin.ModelAdmin):
    list_display = ['level', 'factor_first', 'factor_second']



class MarketingRelationshipAdmin(admin.ModelAdmin):
    list_display = ['user','commission','total_commission','parent_marketer','config','is_freeze','updated_datetime']
    list_filter = ("config","is_freeze")
    search_fields = ('user__name', 'user__username')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'

class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'updated_datetime']
    search_fields = ('name', 'desc')
    ordering = ('updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE



class TeacherApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'apply_status' ,'updated_datetime']
    search_fields = ('user__name', 'user__username')
    list_filter = ["apply_status"]
    ordering = ('-apply_status','updated_datetime',)
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
    ordering = ( 'updated_datetime',)
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'

admin.site.register(MarketerConfigs,MarketerConfigsAdmin)
admin.site.register(MarketingRelationship,MarketingRelationshipAdmin)
admin.site.register(TeacherApplication,TeacherApplicationAdmin)
admin.site.register(Poster,PostAdmin)
admin.site.register(MarketerApplication,MarketerApplicationAdmin)
admin.site.register(MarketingCode,MarketingCodeAdmin)
