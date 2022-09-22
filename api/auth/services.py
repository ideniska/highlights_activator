from dj_rest_auth.jwt_auth import set_jwt_cookies
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.settings import api_settings as jwt_settings
from api.auth.serializers import LoginResponseSerializer

# class LoginService:
#     def __init__(self, request):
#         self.request = request

#     def _authenticate(self, **kwargs):
#         return authenticate(self.request, **kwargs)

#     def validate(self, email: str, password: str):
#         user = self._authenticate(email=email, password=password)
#         if not user:
#             raise ValidationError("Wrong email or password")
#         return user

#     def response(self, user):
#         token = Token.objects.get_or_create(user=user)[0]
#         data = {
#             "token": token.key,
#         }
#         return Response(data)


class LoginService:
    response_serializer = LoginResponseSerializer

    def __init__(self, request):
        self.request = request

    def _authenticate(self, **kwargs):
        return authenticate(self.request, **kwargs)

    def validate(self, email: str, password: str):
        user = self._authenticate(email=email, password=password)
        if not user:
            raise ValidationError("Wrong email or password")
        return user

    def __user_tokens(self, user) -> tuple[str, str]:
        refresh: RefreshToken = RefreshToken.for_user(user)
        return refresh.access_token, str(refresh)

    def response(self, user):
        access_token, refresh_token = self.__user_tokens(user)
        access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        return_expiration_times = getattr(settings, "JWT_AUTH_RETURN_EXPIRATION", False)
        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        if return_expiration_times:
            data["access_token_expiration"] = access_token_expiration
            data["refresh_token_expiration"] = refresh_token_expiration
        serializer = self.response_serializer(data)
        response = Response(serializer.data, status=HTTP_200_OK)
        set_jwt_cookies(response, access_token, refresh_token)
        return response
