from distutils.log import Log
from logging import raiseExceptions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import (
    SignInSerializer,
    SignUpSerializer,
    RefreshTokenSerializer,
    ActivationSerializer,
)
from api.auth import serializers
from .services import LoginService
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from core.tasks import celery_send_html_activation_email, send_information_email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import status
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        current_site = get_current_site(request)
        # celery_send_html_activation_email.delay(user_id=user.id)
        send_information_email(
            subject="Confirm registration",
            template_name="emails/email_confirmation.html",
            context={
                "user": user.email,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.id)),
                "token": default_token_generator.make_token(user),
            },
            to_email=user.email,
            letter_language="en",
        )

        return Response({"detail": True})


User = get_user_model()


class ActivateView(GenericAPIView):
    serializer_class = ActivationSerializer
    permission_classes = ()

    def post(self, request):
        user_id = force_str(urlsafe_base64_decode(request.data["user_id"]))
        confirmation_token = request.data["token"]
        user = User.objects.get(id=user_id)

        if not default_token_generator.check_token(user, confirmation_token):
            return Response(
                "Token is invalid or expired. Please request another confirmation email by signing in.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = True
        user.save()

        service = LoginService(request)

        return service.response(user)


class SignInView(GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = LoginService(request)
        user = service.validate(
            email=serializer.data["email"], password=serializer.data["password"]
        )

        return service.response(user)


class SignOutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = RefreshTokenSerializer

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# TODO update to simple JWT


class UploadApiView(GenericAPIView):
    pass
