from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_engineer = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=True)
    is_editor = models.BooleanField(default=False)
    is_approver = models.BooleanField(default=False)
