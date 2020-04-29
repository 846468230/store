from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
User = get_user_model()
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        g = Group.objects.get(name="member")
        #password = instance.password
        #instance.set_password(password)
        instance.save()
        instance.groups.add(g)