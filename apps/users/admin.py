from django.contrib import admin
from store.settings import ADMIN_LIST_PER_PAGE
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import UserProfile,VerifyCode
from django.utils.translation import gettext, gettext_lazy as _
# Register your models here.

User = get_user_model()

class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ['code','mobile','added_datetime']
    search_fields = ['mobile']
    ordering = ['added_datetime']
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'added_datetime'

class UserChangeForm(UserChangeForm):
    username = forms.CharField(disabled=True,label="用户名")
    class Meta(UserChangeForm.Meta):
        model = User


class UserAdmin(UserAdmin):
    form = UserChangeForm
    list_display = ['username','name','mobile','gender']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    list_per_page = ADMIN_LIST_PER_PAGE
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'nickname', 'avatar','birthday','gender','mobile','email','session_key','openid','id_card_number','id_card_front','id_card_back')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

admin.site.register(VerifyCode,VerifyCodeAdmin)
admin.site.register(User, UserAdmin)



admin.site.site_title="中医课堂"
admin.site.site_header="中医课堂"
admin.site.index_title="中医课堂"
