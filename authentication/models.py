from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    birth_date = models.DateField(blank=False)
    age = models.IntegerField(null=True, blank=True)

    can_be_contacted = models.BooleanField(
        default=False,
        verbose_name="J'autorise SoftDeskSupport à me contacter",
    )
    can_data_be_shared = models.BooleanField(default=False)
