from django.contrib import admin
from store.settings import ADMIN_LIST_PER_PAGE
from .models import CourseCategory, Course, Lesson, Video, CourseResource, Banner, HotSearchWords
from django import forms
from .signals import upload_file
import os
# Register your models here.
admin.site.register([HotSearchWords])
class CourseCategoryForm(forms.ModelForm):
    image = forms.ImageField(required=False,label="分类封面图")
    icon = forms.ImageField(required=False,label="分类图标")
    class Meta:
        model = CourseCategory
        fields = "__all__"

class CourseCategoeryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category_type', 'parent_category', 'is_tab']
    search_fields = ['name', 'code']
    list_filter = ['category_type', 'parent_category']
    ordering = ['updated_datetime']
    list_per_page = ADMIN_LIST_PER_PAGE
    date_hierarchy = 'updated_datetime'
    form =  CourseCategoryForm


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


class VideoForm(forms.ModelForm):
    url = forms.URLField(disabled=True,required=False)
    vod_id = forms.IntegerField(disabled=True,required=False)
    def save(self, commit=True):
        """
        Save this form's self.instance object if commit=True. Otherwise, add
        a save_m2m() method to the form which can be called after the instance
        is saved manually at a later time. Return the model instance.
        """
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        if 'video_file' in self.changed_data:
            name = self.instance.video_file.field.generate_filename(self.instance.video_file.instance, self.instance.video_file.name)
            base_locaton = self.instance.video_file.storage.base_location
            upload_file.send(Video,path = os.path.join(base_locaton,name),instance=self.instance)
        return self.instance

    class Meta:
        model = Video
        fields = '__all__'


class VideoAdmin(admin.ModelAdmin):
    list_display = ['name', 'lesson', 'learn_times','url','updated_datetime']
    search_fields = ['name', 'lesson__name']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['updated_datetime']
    date_hierarchy = 'updated_datetime'
    form = VideoForm


class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'updated_datetime']
    search_fields = ['name', 'course__name']
    list_per_page = ADMIN_LIST_PER_PAGE
    ordering = ['updated_datetime']
    date_hierarchy = 'updated_datetime'


class BannerAdmin(admin.ModelAdmin):
    list_display = ['goods', 'index', 'updated_datetime']
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
