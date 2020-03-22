from .models import UserFav
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver


@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        course = instance.course
        course.fav_nums += 1
        course.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    course = instance.course
    course.fav_nums -= 1
    course.save()