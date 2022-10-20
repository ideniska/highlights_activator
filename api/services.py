import random
from urllib import response
from api.serializers import UserSerializer, QuoteSerializer, BookSerializer
from core.models import Quote, Orders, Book
from core.tasks import celery_stop_membership
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.models import CustomUser, UserType
from rest_framework.response import Response
from rest_framework import status


User: UserType = get_user_model()


def pick_random_quote_id(user):
    start = Quote.objects.filter(owner=user).first().id
    end = Quote.objects.filter(owner=user).last().id
    return random.randrange(start, end)


class ActivateTrialService:
    def activate_trial(self, user):
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


class ChangeUserSettingsService:
    serializer = UserSerializer

    def change_notification_settings(self, user: CustomUser):
        user.send_emails = self.serializer.data["send_emails"]
        user.send_telegrams = self.serializer.data["send_telegrams"]
        user.save()


class ChangeQuoteLikeStatusService:
    serializer = QuoteSerializer

    def change_quote_like_status(self, pk: int):
        try:
            quote = Quote.objects.get(id=pk)
        except Quote.DoesNotExist:
            return Response({"detail": "not found"}, status=404)

        quote.like = not quote.like
        quote.save()
        return Response({"detail": True})


class ChangeBookVisibilityService:
    serializer = BookSerializer

    def change_book_visibility(self, pk: int):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response({"detail": "not found"}, status=404)

        book.visibility = not book.visibility
        book.save()
        return Response({"detail": True})


class GetDailyQuotesQueryset:
    serializer_class = QuoteSerializer

    def get_daily_quotes_queryset(self, user):
        # list of liked quotes id's
        liked_quotes_id_list = list(
            Quote.objects.filter(owner=user)
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

        queryset1 = Quote.objects.filter(owner=user).filter(
            id__in=liked_random_quote_id_list
        )

        # list of all other quotes to show in daily review
        other_quotes_id_list = list(
            Quote.objects.filter(owner=user).values_list("id", flat=True)
        )

        number_of_quotes_to_show = 10 - number_of_fav_quotes
        random_quote_id_list = random.sample(
            other_quotes_id_list,
            min(len(other_quotes_id_list), number_of_quotes_to_show),
        )
        queryset2 = Quote.objects.filter(owner=user).filter(id__in=random_quote_id_list)

        queryset = queryset1.union(queryset2)
        return queryset
