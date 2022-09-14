from distutils.log import Log
from logging import raiseExceptions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import SignInSerializer, SignUpSerializer
from api.auth import serializers
from .services import LoginService
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from core.tasks import celery_send_activation_email, celery_send_html_activation_email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["response"] = "User registered"
            data["email"] = user.email
            current_site = get_current_site(request)
            # celery_send_activation_email.delay(user.email)
            celery_send_html_activation_email(user, current_site)
        else:
            data = serializer.errors

        return Response(data)


class ActivateView(GenericAPIView):
    def get(self, request):
        user_id = request.query_params.get("uid", "")
        print("user_id", user_id)
        confirmation_token = request.query_params.get("token", "")
        print("token", confirmation_token)
        user = self.get_queryset().get(pk=user_id)
        print(user)
        if not default_token_generator.check_token(user, confirmation_token):
            return Response(
                "Token is invalid or expired. Please request another confirmation email by signing in.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = True
        user.save()
        login(request, user)
        return Response("Email successfully confirmed")


class SignInView(GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = ()

    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = LoginService(request)
        user = service.validate(
            email=serializer.data["email"], password=serializer.data["password"]
        )

        return service.response(user)


class SignOutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        data = {"landing-url": reverse("landing", request=request)}
        return Response(data)


# TODO create SignUp view
# TODO update to simple JWT
