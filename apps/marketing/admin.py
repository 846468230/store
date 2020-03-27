from django.contrib import admin
from .models import MarketingRelationship,Poster,TeacherApplication,MarketerApplication,MarketerConfigs,MarketingCode
# Register your models here.
admin.site.register([MarketingRelationship,Poster,TeacherApplication,MarketerApplication,MarketerConfigs,MarketingCode])