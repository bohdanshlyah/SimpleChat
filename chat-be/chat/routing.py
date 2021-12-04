from django.urls import re_path
from django.urls.conf import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:chat_number>', ChatConsumer.as_asgi()),
]