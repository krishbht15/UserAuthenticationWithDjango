from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate

from user import util
from user_auth.roles import Roles


def addDefaultUser(sender, **kwargs):
    User = apps.get_model("user", "User")
    User(username="admin", email="admin@admin.com", password=util.encodePassword("admin"),
         role=Roles.SUPER_ADMIN).save()


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        post_migrate.connect(addDefaultUser, sender=self)
