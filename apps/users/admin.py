from django.contrib import admin
from .models import UserProfile,VerifyCode
# Register your models here.
admin.site.register([UserProfile,VerifyCode])
admin.site.site_title="瑞霖"
admin.site.site_header="瑞霖"
admin.site.index_title="瑞霖"