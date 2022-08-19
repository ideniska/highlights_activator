from turtle import up
from django.db import models
from django.conf import settings
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class FileType(models.TextChoices):
    KINDLE = ("kindle", "Kindle")
    OTHER = ("other", "Other")


def upload_file_path(obj: "UserFile", filename):
    return f"user_files/{obj.owner_id}/{obj.type}/{filename}"


class UserFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_files")
    file = models.FileField("", upload_to=upload_file_path)
    type = models.CharField(choices=FileType.choices, max_length=30)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    title = models.CharField(max_length=350)
    visibility = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.title


class Quote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="quotes")
    date_added = models.CharField(max_length=250)
    text = models.CharField(max_length=1500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quotes")
    like = models.BooleanField(default=False)
