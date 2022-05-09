from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Chat, Message, SheduledMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username",)


class ChatSerializers(serializers.ModelSerializer):
    """ Serilizer for chat """
    creator = UserSerializer()

    class Meta:
        model = Chat
        fields = ("id", "chat_name", "creator")


class MessageSerializer(serializers.ModelSerializer):
    """ Serilizer for messages """
    user = UserSerializer()

    class Meta:
        model = Message
        fields = ("chat", "user", "date", "text")


class MessagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("chat", "text")


class SheduledMessageSerializer(serializers.ModelSerializer):
    """ Serilizer for scheduled messages """
    user = UserSerializer()

    class Meta:
        model = SheduledMessage
        fields = ("chat", "user", "date", "text")


class SheduledPostMessageSerializer(serializers.ModelSerializer):
    """ Serilizer for scheduled messages """

    class Meta:
        model = SheduledMessage
        fields = ("chat", "date", "text")