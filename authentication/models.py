from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    can_be_contacted = models.BooleanField()
    can_be_sharde = models.BooleanField()
    age = models.IntegerField()
