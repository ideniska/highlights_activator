from distutils.log import Log
from logging import raiseExceptions
from urllib import response
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from users.models import CustomUser
from .serializers import (
    SignInSerializer,
    SignUpSerializer,
    RefreshTokenSerializer,
    ActivationSerializer,
    RestorePasswordSerializer,
    SetPasswordSerializer,
)
from .services import LoginService, PasswordService, ActivationService
from core.notifications import EmailService
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework import status
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .services import full_logout
from django.contrib.sites.shortcuts import get_current_site


User = get_user_model()


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        current_site = get_current_site(request)
        email = EmailService()
        email.send_activation_link(user, current_site)
        return Response({"detail": True})


class ActivateView(GenericAPIView):
    serializer_class = ActivationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activation_service = ActivationService()
        user = activation_service.check_email_link(
            uid=serializer.validated_data["uid"],
            token=serializer.validated_data["token"],
        )
        activation_service.set_active(user)
        login_service = LoginService(request)
        return login_service.response(user)


class SignInView(GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = LoginService(request)
        user = service.validate(
            email=serializer.data["email"], password=serializer.data["password"]
        )
        return service.response(user)


class SignOutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RefreshTokenSerializer

    def post(self, request, *args):
        print(request.COOKIES)
        data = {"refresh": request.COOKIES["refresh"]}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = full_logout(request)
        return response


class RestorePassword(GenericAPIView):
    serializer_class = RestorePasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        current_site = get_current_site(request)
        email = EmailService()
        email.send_password_reset(user, current_site)
        return Response({"detail": True})


class SetNewPassword(GenericAPIView):
    serializer_class = SetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = PasswordService()
        user = service.check_email_link(
            uid=serializer.validated_data["uid"],
            token=serializer.validated_data["token"],
        )
        service.set_new_password(user, password=serializer.validated_data["password"])
        return Response({"detail": True})


class SetTgDeepLink:
    pass
