from django.contrib import admin
from .models import UserFav,UserAsk,CourseComments,UserLeavingMessage,UserMessage,UserCourse,UserAddress
# Register your models here.
admin.site.register([UserFav,UserAsk,CourseComments,UserLeavingMessage,UserMessage,UserCourse,UserAddress])