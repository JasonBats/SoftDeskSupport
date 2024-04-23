from django.db import models
from django.contrib.auth.models import AbstractUser
from SoftDeskSupport import utils


class User(AbstractUser):
    can_be_contacted = models.BooleanField(null=False, default=False)
    can_be_shared = models.BooleanField(null=False, default=False)
    birth_date = models.DateField(null=False, blank=False)
    age = utils.get_user_age(birth_date)
