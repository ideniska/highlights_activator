from dataclasses import fields
from turtle import update
from rest_framework import serializers
from core.models import Book, Quote
from users.models import CustomUser
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    quotes_count = serializers.IntegerField()
    book_id = serializers.IntegerField(source="id")

    class Meta:
        model = Book
        fields = ["title", "visibility", "owner", "quotes_count", "book_id"]


class QuoteSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title")
    quote_id = serializers.IntegerField(source="id")
    cover = serializers.CharField(source="book.cover")

    class Meta:
        model = Quote
        fields = ["book", "cover", "date_added", "text", "like", "quote_id", "comment"]


class QuoteUpdateSerializer(serializers.ModelSerializer):
    quote_id = serializers.IntegerField(source="id")

    class Meta:
        model = Quote
        fields = ["quote_id", "text", "comment"]


# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ["paid", "paid_start", "paid_end"]

#     def update(self, instance, validated_data):
#         if self.context["request"].user.paid:
#             return instance
#         self.paid_start = datetime.now()
#         self.paid_end = datetime.now()
#         self.paid = True
#         return super().update(instance, validated_data)
