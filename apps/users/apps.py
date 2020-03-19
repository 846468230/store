from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户管理"

    def ready(self):
        import users.signals
