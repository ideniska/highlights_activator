from api.serializers import QuoteSerializer
from api.services import pick_random_quote_id
from core.models import Book, Quote
from dj_rest_auth.jwt_auth import set_jwt_cookies
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.core import serializers
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from api.auth.serializers import LoginResponseSerializer
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from users.models import CustomUser, UserType


User: UserType = get_user_model()


class TelegramService:
    def validate(self, email: str, telegram_id: int):
        try:
            user = User.objects.get(
                email=force_str(urlsafe_base64_decode(email)), telegram_id=telegram_id
            )
        except:
            raise ValidationError("User not found or account is not connected")
        return user

    def response(self, user):
        quote = Quote.objects.filter(owner=user).get(id=pick_random_quote_id(user))
        serializer = QuoteSerializer(quote)
        return serializer.data
