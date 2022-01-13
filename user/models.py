import uuid
from datetime import datetime

from django.db import models


# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=120)
    role = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=datetime.today())
    updated_at = models.DateTimeField(default=datetime.today())
    deleted_at = models.DateTimeField(default=None)
