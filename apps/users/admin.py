from django.contrib import admin
from store.settings import ADMIN_LIST_PER_PAGE
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import UserProfile, VerifyCode
from marketing.models import MarketingRelationship
from django.utils.translation import gettext, gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
# Register your models here.
from import_export.fields import Field
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import Group

User = get_user_model()


class UserResource(resources.ModelResource):
    username = Field(attribute="user__username", column_name="用户名")
    name = Field(attribute="user__name", column_name="中文名")
    nickname = Field(attribute="nickname", column_name="昵称")
    birthday = Field(attribute="birthday", column_name="生日")
    gender = Field(attribute="gender", column_name="性别")
    mobile = Field(attribute="mobile", column_name="手机号")
    email = Field(attribute="email", column_name="邮箱地址")
    id_card_number = Field(attribute="id_card_number", column_name="身份证号码")

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'nickname', 'birthday', 'gender', 'mobile', 'email', 'id_card_number']
        export_order = ['id', 'username', 'name', 'nickname', 'birthday', 'gender', 'mobile', 'email', 'id_card_number']


class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'mobile', 'added_datetime']
    search_fields = ['mobile']
    ordering = ['added_datetime']
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'added_datetime'


class UserChangeForm(UserChangeForm):
    username = forms.CharField(disabled=True, label="用户名")

    class Meta(UserChangeForm.Meta):
        model = User


class MarketerFilter(SimpleListFilter):
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
            return queryset.filter(id__in=users)
        return queryset


class UserCustomAdmin(ImportExportModelAdmin, UserAdmin):
    form = UserChangeForm
    list_display = ['username', 'name', 'marketer', 'mobile', 'gender']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',MarketerFilter)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    list_per_page = ADMIN_LIST_PER_PAGE
    filter_horizontal = ('groups', 'user_permissions',)
    resource_class = UserResource
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
        'name', 'nickname', 'avatar', 'birthday', 'gender', 'mobile', 'email', 'session_key', 'openid',
        'id_card_number', 'id_card_front', 'id_card_back')}),
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user
        if user.groups.filter(name="market_manager").exists():
            users = MarketingRelationship.objects.all().values("user")
            queryset = queryset.filter(id__in=users)
        return queryset


admin.site.register(VerifyCode, VerifyCodeAdmin)
admin.site.register(User, UserCustomAdmin)

admin.site.site_title = "中医课堂"
admin.site.site_header = "中医课堂"
admin.site.index_title = "中医课堂"
