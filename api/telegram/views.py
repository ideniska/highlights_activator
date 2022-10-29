from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.telegram.services import TelegramService

from django.shortcuts import get_object_or_404 as _get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.services import (
    ActivateTelegramUserService,
)
from api.serializers import ActivateTelegramUserSerializer
from .serializers import TelegramAuthSerializer


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


class TelegramRandomServerQuoteAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = TelegramAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = TelegramService()
        user = service.validate(
            email=serializer.validated_data["email"],
            telegram_id=serializer.validated_data["telegram_id"],
        )
        return Response(service.response(user))
