from urllib import request, response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, authentication
from api.auth.serializers import UploadSerializer
from core.models import Book, Quote
from api.services import pick_random_quote_id
from api.serializers import (
    BookSerializer,
    QuoteSerializer,
    QuoteUpdateSerializer,
    OrdersSerializer,
    UserSerializer,
)
from api.views import RandomServerQuoteAPIView
from users.models import CustomUser
from core.models import Orders

from core.pagination import BasePageNumberPagination
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from core.tasks import celery_stop_membership
from api.services import (
    ActivateTelegramUserService,
)
from api.serializers import ActivateTelegramUserSerializer


class ConnectTelegramBotView(GenericAPIView):
    serializer_class = ActivateTelegramUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activation_service = ActivateTelegramUserService()
        user = activation_service.check_telegram_link(
            telegram_key=serializer.validated_data["telegram_key"]
        )
        activation_service.save_telegram_id(
            user, telegram_id=serializer.validated_data["telegram_id"]
        )
        return Response({"detail": True})


class TelegramRandomServerQuoteAPIView(
    RandomServerQuoteAPIView,
):
    permission_classes = ()
    # authentication_classes =

    def get_queryset(self):
        return Quote.objects.filter(owner=2).filter(
            id=pick_random_quote_id(self.request.user)
        )
