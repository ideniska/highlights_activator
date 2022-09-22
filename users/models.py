from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField("Email address", unique=True)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = []

    def str(self):
        return self.email
