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
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []
    objects = UserManager()  # type: ignore

    def str(self):
        return self.email
