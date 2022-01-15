import uuid

from django.db import models
import datetime

# Create your models here.
from django.db.models import TextChoices

from user import util
from user_auth.roles import Roles


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=120)
    role = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in Roles], null=True)
    created_at = models.DateTimeField(default=datetime.datetime.utcnow())
    updated_at = models.DateTimeField(default=datetime.datetime.utcnow())
    deleted_at = models.DateTimeField(default=None, null=True)
    jwt = models.CharField(max_length=100, default=None, null=True)
