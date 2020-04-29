import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
import django

django.setup()
from django.contrib.auth.models import Group, Permission
from marketing.models import MarketerConfigs

GROUPS = ['admin', 'marketer', 'teacher', 'insider', 'member','market_manager','course_manager','financial_manager']  # 管理员，销售人员，老师，内部人员，普通会员
admin_permissions = ['change_userprofile', 'add_userprofile', 'view_userprofile', 'add_verifycode', 'change_verifycode',
                     'view_verifycode', 'view_usermessage', 'delete_usermessage', 'change_usermessage',
                     'add_usermessage', 'view_userleavingmessage', 'delete_userleavingmessage',
                     'add_userleavingmessage', 'view_userfav', 'view_usercourse', 'delete_usercourse',
                     'change_usercourse', 'add_usercourse', 'view_userask', 'delete_userask', 'view_useraddress',
                     'view_coursecomments', 'change_coursecomments', 'delete_coursecomments', 'add_coursecomments',
                     'view_shoppingcart', 'view_orderinfo', 'view_ordergoods', 'change_orderinfo', "add_banner",
                     "add_course", "add_coursecategory", "add_courseresource", "add_hotsearchwords", "add_lesson",
                     "add_video", "change_banner", "change_course", "change_coursecategory", "change_courseresource",
                     "change_hotsearchwords", "change_lesson", "change_video", "delete_banner", "delete_course",
                     "delete_coursecategory", "delete_courseresource", "delete_hotsearchwords", "delete_lesson",
                     "delete_video", "view_banner", "view_course", "view_coursecategory", "view_courseresource",
                     "view_hotsearchwords", "view_lesson", "view_video","add_marketerapplication","add_marketingrelationship","add_poster","add_teacherapplication","change_marketerapplication","change_marketerconfigs","change_marketingrelationship","change_poster","change_teacherapplication","delete_marketerapplication","delete_poster","delete_teacherapplication","view_marketerapplication","view_marketerconfigs","view_marketingcode","view_marketingrelationship","view_poster","view_teacherapplication"]
marketer_permissions = ["add_marketingcode","delete_marketingcode","view_marketerapplication","view_marketingcode","view_marketingrelationship","view_poster"]
teacher_permissions = ["view_userprofile", "view_usercourse", "view_coursecomments", "view_course",
                       "view_courseresource", "view_lesson", "view_video", "add_course",
                       "add_courseresource", "add_lesson", "add_video"]
insider_permissions = ["view_userprofile"]
member_permissions =[] #['view_userprofile', 'change_userprofile', "add_useraddress", "add_coursecomments", "add_userask",
#                       "add_userfav", "add_userleavingmessage", "change_coursecomments", "change_useraddress",
#                       "change_userask", "change_userleavingmessage", "delete_coursecomments", "delete_useraddress",
#                       "delete_userask", "delete_userfav", "delete_userleavingmessage", "view_coursecomments",
#                       "view_useraddress", "view_userask", "view_usercourse", "view_userfav", "view_userleavingmessage",
#                       "view_usermessage", "add_shoppingcart", "change_shoppingcart", "delete_shoppingcart",
#                       "view_ordergoods", "view_orderinfo", "view_shoppingcart", "view_banner", "view_course",
#                       "view_coursecategory", "view_courseresource", "view_hotsearchwords", "view_lesson", "view_video","add_marketerapplication","add_teacherapplication","view_marketerapplication","view_teacherapplication"]
market_manager_permissions = ["view_poster","add_poster","change_poster","delete_poster","delete_marketingcode","view_marketingcode","add_marketingcode", "view_userprofile",
                              "view_orderinfo", "view_ordergoods"]

course_manager_permissions = ["add_banner","add_course", "add_coursecategory", "add_courseresource", "add_hotsearchwords", "add_lesson",
                     "add_video", "change_banner", "change_course", "change_coursecategory", "change_courseresource",
                     "change_hotsearchwords", "change_lesson", "change_video", "delete_banner", "delete_course",
                     "delete_coursecategory", "delete_courseresource", "delete_hotsearchwords", "delete_lesson",
                     "delete_video", "view_banner", "view_course", "view_coursecategory", "view_courseresource",
                     "view_hotsearchwords", "view_lesson", "view_video"]

financial_manager_permissions = ["view_orderinfo", "view_ordergoods","view_userprofile","view_usercashwithdrawal","add_usercashwithdrawal","change_usercashwithdrawal","delete_usercashwithdrawal","view_marketingrelationship","change_marketingrelationship","view_teachermanagement","change_teachermanagement"]
for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)

for codename in admin_permissions:
    g = Group.objects.get(name="admin")
    p = Permission.objects.get(codename=codename)
    g.permissions.add(p)

for codename in marketer_permissions:
    g = Group.objects.get(name="marketer")
    p = Permission.objects.get(codename=codename)
    g.permissions.add(p)

for codename in teacher_permissions:
    g = Group.objects.get(name="teacher")
    p = Permission.objects.get(codename=codename)
    g.permissions.add(p)

for codename in insider_permissions:
    g = Group.objects.get(name="insider")
    p = Permission.objects.get(codename=codename)
    g.permissions.add(p)

for codename in member_permissions:
    g = Group.objects.get(name="member")
    p = Permission.objects.get(codename=codename)
    g.permissions.add(p)

configs = [(1,0.1,0.05),(2,0.2,0.1),(3,0.3,0.15)]
for item in configs:
    config = MarketerConfigs.objects.get_or_create(level=item[0])

for codename in course_manager_permissions:
    g = Group.objects.get(name='course_manager')
    p = Permission.objects.get(codename=codename)
    g.permissions.add(p)

for codename in market_manager_permissions:
    g = Group.objects.get(name="market_manager")
    p = Permission.objects.get(codename=codename)
    g.permissions.add(p)

for codename in financial_manager_permissions:
    g = Group.objects.get(name="financial_manager")
    p = Permission.objects.get(codename=codename)
    g.permissions.add(p)