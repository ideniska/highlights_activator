from urllib import request
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class LoginService:
    def __init__(self, request):
        self.request = request

    def _authenticate(self, **kwargs):
        return authenticate(self.request, **kwargs)

    def validate(self, email: str, password: str):
        user = self._authenticate(email=email, password=password)
        if not user:
            raise ValidationError("Wrong email or password")
        return user

    def response(self, user):
        token = Token.objects.get_or_create(user=user)
        data = {
            "token": token.key,
        }
        return Response(data)


# TODO create user token with auth.token,
