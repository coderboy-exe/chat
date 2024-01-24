# chat/consumers.py
import json

from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from django.contrib.auth.models import AnonymousUser
from channels.auth import login

import uuid

from .models import UserModel, Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        # api_key = self.scope.get('query_string', b'').decode('utf-8').split('=')[-1]
        # print(api_key)
        
        user = await self.get_user(self.scope['user'].id)
        print("TEST USER ANON", user)
        if user.is_anonymous:
            user = uuid.uuid4()
            self.user = user
            print(user)
            
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Find or create the room
        self.room = await self.get_or_create_room(self.room_group_name)

        # Join room group
        await (self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await (self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # recipient_id = text_data_json["recipient_id"]
        
         # save message in database
        await self.save_message(message)
        
        # Send message to room group
        await (self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat.message", 
                "message": message,
                "sender": str(self.user)[:-4]
                }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": str(event["sender"])
            }))
        
        
    @database_sync_to_async
    def get_user(self, user_id):
        """_summary_

        Args:
            user (_type_): _description_
        """
        try:
            return UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return AnonymousUser()
        
    @database_sync_to_async
    def get_or_create_room(self, room_name):
        room, created = Room.objects.get_or_create(name=room_name)
        return room
    
    @database_sync_to_async
    def save_message(self, content):
        Message.objects.create(
            sender=self.user,
            content=content,
            room=self.room
            )
    
    