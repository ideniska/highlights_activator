from email.policy import default
from typing import TypeVar
from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from .managers import UserManager

UserType = TypeVar("UserType", bound="CustomUser")


class CustomUser(AbstractUser):
    # username = None  # type: ignore
    email = models.EmailField("Email address", unique=True)
    active_subscription = models.BooleanField(default=False)
    trial_used = models.BooleanField(default=False)
    paid_until = models.DateTimeField(null=True, blank=True)
    stripe_session_id = models.CharField(max_length=150, null=True, blank=True)
    send_emails = models.IntegerField(default=1)  # 1 - every day, 2 - weekly
    send_telegrams = models.IntegerField(default=3)  # 1 - every day, 2 - weekly
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []
    objects = UserManager()  # type: ignore

    def str(self):
        return self.email
