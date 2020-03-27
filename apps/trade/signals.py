from .models import OrderInfo
from user_operation.models import UserCourse
from .models import TeacherManagement
from marketing.models import TeacherApplication
from django.db.models.signals import post_save
from django.dispatch import receiver
from marketing.models import MarketingCode,MarketingRelationship,MarketerConfigs
from .models import TeacherManagement

@receiver(post_save, sender=OrderInfo,dispatch_uid="user_course_updated")
def create_user_course(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.user
        if instance.pay_status == OrderInfo.ORDER_STATUS[0][0]:
            for ordergood in instance.ordergoods.all():
                usercourse,creat = UserCourse.objects.get_or_create(user=user, course=ordergood.goods)


@receiver(post_save, sender=TeacherApplication, dispatch_uid="teacher_management_creat")
def create_teacher_application(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.user
        if instance.apply_status == TeacherApplication.APPLICATION_STATUS[0][0]:
            teacher_manager = TeacherManagement.objects.get_or_create(user=user)


@receiver(post_save, sender=OrderInfo,dispatch_uid="marketer_commission_updated")
def update_marketer_commission(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.user
        if instance.pay_status == OrderInfo.ORDER_STATUS[0][0]:
            price = instance.order_mount
            if MarketingCode.objects.filter(code=instance.marketing_code).exists():
                marketer = MarketingCode.objects.filter(code=instance.marketing_code).first().user
                marketer_relationship = marketer.user_marketer
                if not MarketingRelationship.objects.filter(user=user).exists():
                    config = MarketerConfigs.objects.get(level=MarketerConfigs.LEVEL[0][0])
                    MarketingRelationship.objects.get_or_create(user=user, commission=0.0, parent_marketer=marketer,config=config,
                                                                is_freeze=False)
                if not marketer_relationship.is_freeze:
                    marketer_relationship.commission += price * marketer_relationship.config.factor_first
                    marketer_relationship.save()
                parent_marketer = marketer_relationship.parent_marketer
                if parent_marketer and not parent_marketer.user_marketer.is_freeze:
                    parent_marketer.user_marketer.commission+= price * parent_marketer.user_marketer.config.factor_second
                    parent_marketer.user_marketer.save()


@receiver(post_save, sender=OrderInfo,dispatch_uid="teacher_commission_updated")
def update_teacher_commission(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.user
        if instance.pay_status == OrderInfo.ORDER_STATUS[0][0]:
            for ordergood in instance.ordergoods.all():
                course = ordergood.goods
                price = course.price
                teacher_commission = course.teacher.teacher_commission
                teacher_commission.commission += price * teacher_commission.scale_factor
                teacher_commission.save()
