import json
from re import U
from urllib import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, authentication
from api.auth.serializers import UploadSerializer
from core.models import Book, Quote
from .serializers import (
    BookSerializer,
    QuoteSerializer,
    QuoteUpdateSerializer,
)
from users.models import CustomUser
from core.models import Orders

from core.pagination import BasePageNumberPagination
from django.db.models import Count
import random
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone
from core.tasks import celery_stop_membership


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
    pagination_class = BasePageNumberPagination

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

    # authentication_classes = [
    # #     authentication.SessionAuthentication,
    # #     authentication.TokenAuthentication,
    # # ]
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


class QuoteDeleteView(generics.DestroyAPIView):

    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()
    lookup_field = "pk"

    def perform_destroy(self, instance):
        # instance
        super().perform_destroy(instance)


class QuoteUpdateView(generics.UpdateAPIView):

    serializer_class = QuoteUpdateSerializer
    queryset = Quote.objects.all()
    lookup_field = "pk"


class DailyTenAPIView(
    generics.ListCreateAPIView,
):

    serializer_class = QuoteSerializer

    def get_queryset(self):
        # list of liked quotes id's
        liked_quotes_id_list = list(
            Quote.objects.filter(owner=self.request.user)
            .filter(like=True)
            .values_list("id", flat=True)
        )

        liked_quotes_count = len(liked_quotes_id_list)

        # If user has less then 30 liked quotes we don't show them in daily review
        # because they will be shown too frequently
        if liked_quotes_count > 60:
            number_of_fav_quotes = 2

        elif 30 <= liked_quotes_count < 60:
            number_of_fav_quotes = 1

        else:
            number_of_fav_quotes = 0

        liked_random_quote_id_list = random.sample(
            liked_quotes_id_list, min(liked_quotes_count, number_of_fav_quotes)
        )

        queryset1 = Quote.objects.filter(owner=self.request.user).filter(
            id__in=liked_random_quote_id_list
        )

        # list of all other quotes to show in daily review
        other_quotes_id_list = list(
            Quote.objects.filter(owner=self.request.user).values_list("id", flat=True)
        )

        number_of_quotes_to_show = 10 - number_of_fav_quotes
        random_quote_id_list = random.sample(
            other_quotes_id_list,
            min(len(other_quotes_id_list), number_of_quotes_to_show),
        )
        queryset2 = Quote.objects.filter(owner=self.request.user).filter(
            id__in=random_quote_id_list
        )

        queryset = queryset1.union(queryset2)
        return queryset


class UploadApiView(GenericAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer

    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivateTrialApiView(APIView):
    def get(self, request):
        user = request.user
        if not user.active_subscription and not user.trial_used:
            user.active_subscription = True
            user.trial_used = True
            order = Orders.objects.create(
                user=user,
                order_type="Trial",
                subscription_period=60,
                price=0,
                payment_date=timezone.now(),
                payment_status="active",
            )
            user.save()
            order.save()
            celery_stop_membership.apply_async(
                kwargs={"user_id": user.id}, countdown=order.subscription_period
            )
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"Fail": "Trial already in use or finished"},
            status=status.HTTP_400_BAD_REQUEST,
        )
