from queue import Empty
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField("Email address", unique=True)
    active_subscription = models.BooleanField(default=False)
    trial_used = models.BooleanField(default=False)
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []

    def str(self):
        return self.email
