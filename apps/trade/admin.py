from django.contrib import admin
from .models import ShoppingCart,OrderInfo,OrderGoods,TeacherManagement

# Register your models here.
admin.site.register([ShoppingCart,OrderInfo,OrderGoods,TeacherManagement])
