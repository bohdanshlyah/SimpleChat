import json
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
            chat_inst = Chat(chat)
            SheduledMessage.objects.create(chat=chat_inst, date=date, text=text, user=user)

            dialog = MessagePostSerializer(data={'chat': chat, 'text': 'Sorry, postponing messages is not available yet'})
            if dialog.is_valid():
                await database_sync_to_async(dialog.save)(user=user)
            mess = await self.get_last_message() 
            serializer = MessageSerializer(mess)
            
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
    def get_last_message(self):
        return Message.objects.latest('date')