from rest_framework import serializers
from core.models import Book, Quote


class BookSerializer(serializers.ModelSerializer):
    quotes_count = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ["title", "visibility", "owner", "quotes_count"]


class QuoteSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title")

    class Meta:
        model = Quote
        fields = ["book", "date_added", "text"]
