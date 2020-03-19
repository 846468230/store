import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+'../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

import django
django.setup()

from goods.models import Course,CourseCategory
from django.contrib.auth import  get_user_model
from db_tools.data.product_data import row_data

User = get_user_model()
for goods_detail in row_data:
    goods = Course()
    goods.name = goods_detail["name"]
    goods.desc = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    teahcer = User.objects.filter(id=1)[0]
    goods.teacher = teahcer
    goods.degree = 'cj'
    goods.image = goods_detail["images"][0] if goods_detail["images"] else ""
    goods.detail = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""


    category_name = goods_detail["categorys"][-1]
    category = CourseCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

