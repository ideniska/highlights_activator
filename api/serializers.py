from rest_framework import serializers
from core.models import Book, Quote


class BookSerializer(serializers.ModelSerializer):
    quotes_count = serializers.IntegerField()
    book_id = serializers.IntegerField(source="id")

    class Meta:
        model = Book
        fields = ["title", "visibility", "owner", "quotes_count", "book_id"]


class QuoteSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title")
    quote_id = serializers.IntegerField(source="id")

    class Meta:
        model = Quote
        fields = ["book", "date_added", "text", "like", "quote_id", "comment"]


class QuoteUpdateSerializer(serializers.ModelSerializer):
    quote_id = serializers.IntegerField(source="id")

    class Meta:
        model = Quote
        fields = ["quote_id", "text", "comment"]
