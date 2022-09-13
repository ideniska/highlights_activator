from tkinter.ttk import Style
from rest_framework import serializers
from users.models import CustomUser


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={"input_type:": "password"}, write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ["email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = CustomUser(
            email=self.validated_data["email"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValueError({"password": "Passwords must match."})
        user.set_password(password)
        user.save()
        return user
