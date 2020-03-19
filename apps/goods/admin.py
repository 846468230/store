from django.contrib import admin
from .models import CourseCategory,Course,Lesson,Video,CourseResource,Banner,HotSearchWords
# Register your models here.
admin.site.register([CourseCategory,Course,Lesson,Video,CourseResource,Banner,HotSearchWords])
