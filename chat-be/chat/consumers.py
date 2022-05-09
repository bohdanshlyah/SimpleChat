import json
import time
import threading
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token

from .serializers import MessagePostSerializer, MessageSerializer, UserSerializer, SheduledMessageSerializer, SheduledPostMessageSerializer
from .models import Chat, Message, SheduledMessage

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_number']
        self.chat_group_name = 'chat_%s' % self.chat_name

        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, data):
        token_key = data['token']
        user = await self.get_user(token_key)
        chat = data['chat']
        text = data['text']
        date = data['datetime']
        if date == '':
            dialog = MessagePostSerializer(data={'chat': chat, 'text': text})
            if dialog.is_valid():
                await database_sync_to_async(dialog.save)(user=user)
            mess = await self.get_last_message() 
            serializer = MessageSerializer(mess)
        else:
            date_time_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M")
            date = date_time_obj-timedelta(hours=2)
            dialog = SheduledPostMessageSerializer(data={'chat': chat, 'text': text, 'date': date})
            if dialog.is_valid():
                await database_sync_to_async(dialog.save)(user=user)
            mess = await self.get_last_message(sched=True)
            await self.sending_delay(mess)
            serializer = SheduledMessageSerializer(mess)
            
        message = serializer.data

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message
                
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_user(self, token_key):
        return Token.objects.get(key=token_key).user

    @database_sync_to_async
    def get_last_message(self, sched=False):
        if sched:
            return SheduledMessage.objects.latest('id')
        else:
            return Message.objects.latest('date')
    

    async def sending_delay(self, mess):
        now = datetime.now()
        delay = (mess.date - now).total_seconds()
        print(delay)
        if delay > 0:
            await asyncio.sleep(delay)
            # time.sleep(delay)
