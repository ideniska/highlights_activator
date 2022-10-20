from email.policy import default
from enum import unique
from tkinter import DISABLED
from typing import TypeVar
from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from .managers import UserManager

UserType = TypeVar("UserType", bound="CustomUser")


class NotificationSetting(models.IntegerChoices):
    DAILY = (1, "Daily")
    WEEKLY = (2, "Weekly")
    DISABLED = (3, "Disabled")


class CustomUser(AbstractUser):
    # username = None  # type: ignore
    email = models.EmailField("Email address", unique=True)
    active_subscription = models.BooleanField(default=False)
    trial_used = models.BooleanField(default=False)
    paid_until = models.DateTimeField(null=True, blank=True)
    stripe_session_id = models.CharField(
        max_length=150, null=True, blank=True, unique=True
    )
    send_emails = models.PositiveSmallIntegerField(
        default=NotificationSetting.DAILY, choices=NotificationSetting.choices
    )
    send_telegrams = models.PositiveSmallIntegerField(
        default=NotificationSetting.DISABLED, choices=NotificationSetting.choices
    )
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []
    objects = UserManager()  # type: ignore

    def str(self):
        return self.email
