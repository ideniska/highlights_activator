from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type:": "password"}, min_length=8)
    password2 = serializers.CharField()

    def validate_email(self, email: str):
        user = CustomUser.objects.filter(email=email)
        if user:
            raise serializers.ValidationError("User with this email already exists.")
        return email

    def validate_password(self, password: str):
        validate_password(password)
        return password

    def validate(self, attrs: dict):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def save(self):
        # user = CustomUser(
        #     email=self.validated_data["email"],
        #     username=self.validated_data["email"],
        # )
        # password = self.validated_data["password"]
        # password2 = self.validated_data["password2"]

        user = CustomUser.objects.create_user(
            email=self.validated_data["email"],
            username=self.validated_data["email"],
            password=self.validated_data["password"],
        )

        # user.set_password(password)
        user.is_active = False
        user.save()
        return user


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    access_token_expiration = serializers.DateTimeField(required=False)
    refresh_token_expiration = serializers.DateTimeField(required=False)


class ActivationSerializer(serializers.Serializer):
    def validate(self, attrs):
        return super().validate(attrs)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"bad_token": _("Token is invalid or expired")}

    def validate(self, attrs):
        print(attrs)
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
