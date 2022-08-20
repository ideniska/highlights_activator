import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, authentication
from core.models import Book, Quote
from .serializers import BookSerializer, QuoteSerializer

from core.pagination import BasePageNumberPagination
from django.db.models import Count
import random
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    return Response(request.data)


class BookListAPIView(
    generics.ListCreateAPIView,
):

    serializer_class = BookSerializer
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        queryset = (
            Book.objects.filter(owner=self.request.user)
            .annotate(quotes_count=Count("quotes"))
            .order_by("-quotes_count")
        )
        return queryset


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = (
            Book.objects.filter(owner=self.request.user)
            .annotate(quotes_count=Count("quotes"))
            .order_by("-quotes_count")
        )
        return queryset


# class QuotesFromBookAPIView(generics.RetrieveAPIView):

#     lookup_field = "book.id"
#     serializer_class = QuoteSerializer

#     def get_queryset(self):
#         queryset = Quote.objects.filter(owner=self.request.user)
#         return queryset


class QuotesFromBookAPIView(generics.ListAPIView):

    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(owner=self.request.user)
            .filter(book_id=self.kwargs["pk"])
        )


# For RandomServerQuoteAPIView
def pick_random_object(user):
    start = Quote.objects.filter(owner=user).first().id
    end = Quote.objects.filter(owner=user).last().id
    return random.randrange(start, end)


class RandomServerQuoteAPIView(
    generics.ListAPIView,
):

    serializer_class = QuoteSerializer

    def get_queryset(self):
        return Quote.objects.filter(owner=self.request.user).filter(
            id=pick_random_object(self.request.user)
        )


class FavoriteQuotesAPIView(
    generics.ListCreateAPIView,
):

    serializer_class = QuoteSerializer

    def get_queryset(self):
        queryset = Quote.objects.filter(owner=self.request.user).filter(like=True)
        return queryset


class BookVisibilityView(generics.GenericAPIView):

    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def post(self, request, pk: int):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response({"detail": "not found"}, status=404)

        book.visibility = not book.visibility
        book.save()
        return Response({"detail": True})


# TODO Ask Nazarii to update BookVisibilityView: filter.exists() if yes .update() -- more optimal way update visibility status from db


class QuoteLikeView(generics.GenericAPIView):

    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

    def post(self, request, pk: int):
        try:
            quote = Quote.objects.get(id=pk)
        except Quote.DoesNotExist:
            return Response({"detail": "not found"}, status=404)

        quote.like = not quote.like
        quote.save()
        return Response({"detail": True})
