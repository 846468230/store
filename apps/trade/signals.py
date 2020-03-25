from .models import OrderInfo
from user_operation.models import UserCourse
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=OrderInfo,dispatch_uid="user_course_updated")
def create_user_course(sender, instance=None, created=False, **kwargs):
    if created:
        pass#instance.save()
    else:
        user = instance.user
        if instance.pay_status == OrderInfo.ORDER_STATUS[0][0]:
            for ordergood in instance.ordergoods.all():
                usercourse,creat = UserCourse.objects.get_or_create(user=user, course=ordergood.goods)
