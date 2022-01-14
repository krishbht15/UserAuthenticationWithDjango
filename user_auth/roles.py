from enum import Enum

from django.db.models import TextChoices


class Roles(TextChoices):
    READ_ONLY = "READ_ONLY"
    FULL_MEMBERS = "FULL_MEMBERS"
    SUPER_ADMIN = "SUPER_ADMIN"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
