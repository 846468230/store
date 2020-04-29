from .models import OrderInfo
from user_operation.models import UserCourse
from .models import TeacherManagement
from marketing.models import TeacherApplication
from django.db.models.signals import post_save
from django.dispatch import receiver
from marketing.models import MarketingCode, MarketingRelationship, MarketerConfigs
from .models import TeacherManagement,OrderGoods
import datetime


@receiver(post_save, sender=OrderInfo, dispatch_uid="user_course_updated")
def create_user_course(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.user
        if instance.pay_status == OrderInfo.ORDER_STATUS[0][0]:
            for ordergood in instance.ordergoods.all():
                usercourse, creat = UserCourse.objects.get_or_create(user=user, course=ordergood.goods)


@receiver(post_save, sender=TeacherApplication, dispatch_uid="teacher_management_creat")
def create_teacher_application(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.user
        if instance.apply_status == TeacherApplication.APPLICATION_STATUS[0][0]:
            teacher_manager = TeacherManagement.objects.get_or_create(user=user)


def update_commission(parent_marketer, price):
    if not parent_marketer:
        return
    if not parent_marketer.user_marketer:
        return
    marketer_relationship = parent_marketer.user_marketer
    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=60)
    if MarketingRelationship.objects.filter(parent_marketer=parent_marketer).filter(
        added_datetime__gte=start).exists():
        marketer_relationship.commission += price * marketer_relationship.config.factor_first
        marketer_relationship.total_commission += price * marketer_relationship.config.factor_first
        marketer_relationship.is_freeze = False
    else:
        marketer_relationship.is_freeze = True
    marketer_relationship.save()
    # parent_marketer = marketer_relationship.parent_marketer
    # if parent_marketer and not parent_marketer.user_marketer.is_freeze:
    #    parent_marketer.user_marketer.commission += price * parent_marketer.user_marketer.config.factor_second
    #    parent_marketer.user_marketer.total_commission += price * parent_marketer.user_marketer.config.factor_second
    #    parent_marketer.user_marketer.save()


@receiver(post_save, sender=OrderGoods, dispatch_uid="marketer_commission_updated")
def update_marketer_commission(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.order.user
        if instance.confirm == OrderGoods.CONFIRM_STATUS[1][0]:
            price = instance.goods.price
            if MarketingCode.objects.filter(code=instance.order.marketing_code).exists():
                marketer = MarketingCode.objects.filter(code=instance.order.marketing_code).first().user
                if user == marketer:
                    update_commission(user.user_marketer.parent_marketer, price)
                else:
                    marketing_relationship, created = MarketingRelationship.objects.get_or_create(user=user)
                    if not marketing_relationship.parent_marketer:
                        marketing_relationship.parent_marketer = marketer
                    if not marketing_relationship.config:
                        config = MarketerConfigs.objects.get(level=MarketerConfigs.LEVEL[0][0])
                        marketing_relationship.config = config
                    marketing_relationship.save()
                    update_commission(marketing_relationship.parent_marketer, price)
            elif MarketingRelationship.objects.filter(user=user).exists():
                marketer = MarketingRelationship.objects.filter(user=user).first()
                update_commission(marketer.parent_marketer, price)


@receiver(post_save, sender=OrderGoods, dispatch_uid="teacher_commission_updated")
def update_teacher_commission(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.order.user
        if instance.confirm == OrderGoods.CONFIRM_STATUS[1][0]:
            #for ordergood in instance.ordergoods.all():
            course = instance.goods
            price = course.price
            teacher_commission = course.teacher.teacher_commission
            teacher_commission.commission += price * teacher_commission.scale_factor
            teacher_commission.total_commission += price * teacher_commission.scale_factor
            teacher_commission.save()
