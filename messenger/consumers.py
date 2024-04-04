from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from user_management.models import User
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room_group_name = None

    async def connect(self):
        # Khởi tạo room_group_name
        self.room_group_name = 'chat_superusers'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    async def disconnect(self, close_code):
        # Kiểm tra xem room_group_name đã được khởi tạo hay chưa
        if self.room_group_name is not None:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['recipient']

        # Save message to database asynchronously
        recipient = await self.get_user(username=receiver)
        sender = await self.get_user(username=sender)

        await self.create_message(sender=sender, recipient=recipient, content=message)

        # Send message to all superusers
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username  # Corrected variable name
            }
        )

    @database_sync_to_async
    def create_message(self, sender, recipient, content):
        return Message.objects.create(sender=sender, recipient=recipient, content=content)

    @database_sync_to_async
    def get_superuser(self, username):
        return User.objects.get(username=username)

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
