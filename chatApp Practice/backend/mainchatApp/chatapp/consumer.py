import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.employee_id = self.scope["url_route"]["kwargs"]["employee_id"]
        self.room_group_name = "chat_general"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        employee_id = text_data_json["employee_id"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "employee_id": employee_id}
        )
        
        # Save message to database
        await self.save_message(employee_id, message)

    async def chat_message(self, event):
        message = event["message"]
        employee_id = event["employee_id"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "employee_id": employee_id}))

    @database_sync_to_async
    def save_message(self, employee_id, message):
        user = User.objects.get(id=employee_id)
        ChatMessage.objects.create(user=user, message=message)
