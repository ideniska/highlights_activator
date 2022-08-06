from django.db import models
from django.conf import settings


class UserFiles(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField("", upload_to="user_uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    book_title_db = models.CharField(max_length=350)
    show_status = models.IntegerField(default=1)
    owner = models.IntegerField()

    @classmethod
    def create(cls, book_title_db, owner):
        book = cls(book_title_db=book_title_db, owner=owner)
        return book

    def __str__(self):
        return self.book_title_db


class Quote(models.Model):
    book_title_db = models.ForeignKey("Book", on_delete=models.CASCADE)
    date_added_db = models.CharField(max_length=250)
    quote_db = models.CharField(max_length=1500)
    owner = models.IntegerField()

    @classmethod
    def create(cls, book_title_db, date_added_db, quote_db, owner):
        quote = cls(
            book_title_db=book_title_db,
            date_added_db=date_added_db,
            quote_db=quote_db,
            owner=owner,
        )
        return quote
