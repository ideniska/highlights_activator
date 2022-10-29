from rest_framework import serializers


class TelegramAuthSerializer(serializers.Serializer):
    email = serializers.CharField()
    telegram_id = serializers.IntegerField()
