from .models import MarketerApplication, TeacherApplication
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from user_operation.models import UserMessage
from .models import MarketingRelationship,MarketerConfigs


@receiver(post_save, sender=TeacherApplication, dispatch_uid="teacher_application_updated")
def create_teacher_application(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.user
        g = Group.objects.get(name='teacher')
        if instance.apply_status == TeacherApplication.APPLICATION_STATUS[0][0]:
            user.groups.add(g)
            message = UserMessage.objects.get_or_create(user=user.id, message="恭喜您，您的教师身份申请已通过！", has_read=False)
        elif instance.apply_status == TeacherApplication.APPLICATION_STATUS[1][0]:
            message = UserMessage.objects.get_or_create(user=user.id, message="很遗憾，您的教师身份申请未通过,请核实本人的身份信息重试。", has_read=False)


@receiver(post_save, sender=MarketerApplication, dispatch_uid="marketer_application_updated")
def create_marketer_application(sender, instance=None, created=False, **kwargs):
    if created:
        pass
    else:
        user = instance.user
        g = Group.objects.get(name="marketer")
        if instance.apply_status == MarketerApplication.APPLICATION_STATUS[0][0]:
            user.groups.add(g)
            message,message_created = UserMessage.objects.get_or_create(user=user.id, message="恭喜您，您的课程代表身份申请已通过！", has_read=False)
            config = MarketerConfigs.objects.get(level=MarketerConfigs.LEVEL[0][0])
            mr,created = MarketingRelationship.objects.get_or_create(user=user)
            if created:
                mr.config = config
            mr.parent_marketer = None
            mr.save()
        elif instance.apply_status == MarketerApplication.APPLICATION_STATUS[1][0]:
            message = UserMessage.objects.get_or_create(user=user.id, message="很遗憾，您的课程代表身份申请未通过,请核实本人的身份信息重试。", has_read=False)