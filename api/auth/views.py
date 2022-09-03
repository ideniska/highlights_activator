from distutils.log import Log
from logging import raiseExceptions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import SignInSerializer
from api.auth import serializers
from .services import LoginService


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
