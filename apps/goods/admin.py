from django.contrib import admin
from store.settings import ADMIN_LIST_PER_PAGE
from .models import CourseCategory, Course, Lesson, Video, CourseResource, Banner, HotSearchWords

# Register your models here.
admin.site.register([HotSearchWords])


class CourseCategoeryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category_type', 'parent_category', 'is_tab']
    search_fields = ['name', 'code']
    list_filter = ['category_type', 'parent_category']
    ordering = ['updated_datetime']
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'price', 'degree', 'category', 'online', 'tag', 'updated_datetime']
    search_fields = ['name', 'desc', 'detail', 'teacher__username', 'teacher__name', 'price', 'category__name', 'tag']
    list_filter = ['degree', 'online']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['updated_datetime']
    date_hierarchy = 'updated_datetime'


class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'index', 'updated_datetime']
    search_fields = ['name', 'course__name']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['updated_datetime']
    date_hierarchy = 'updated_datetime'


class VideoAdmin(admin.ModelAdmin):
    list_display = ['name', 'lesson', 'learn_times', 'updated_datetime']
    search_fields = ['name', 'lesson__name']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['updated_datetime']
    date_hierarchy = 'updated_datetime'


class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'course','updated_datetime']
    search_fields = ['name', 'course__name']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['updated_datetime']
    date_hierarchy = 'updated_datetime'


class BannerAdmin(admin.ModelAdmin):
    list_display = ['goods', 'index','updated_datetime']
    search_fields = ['goods__name']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['updated_datetime']
    date_hierarchy = 'updated_datetime'


admin.site.register(CourseCategory, CourseCategoeryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)
admin.site.register(Banner, BannerAdmin)
