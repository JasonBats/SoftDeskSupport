from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    birth_date = models.DateField(null=False, blank=False)
    age = models.IntegerField(null=True, blank=True)

    can_be_contacted = models.BooleanField(
        null=False,
        default=False,
        verbose_name="J'autorise SoftDeskSupport à me contacter",
    )
    can_be_shared = models.BooleanField(null=False, default=False)
