import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from chat.entities.message import Message
from chat.entities.chat_rooms import ChatRoom
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):



    async def check_count(self):
        pass



    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chat_{self.id}'
        room = await sync_to_async(ChatRoom.objects.get)(id = id)

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,

        )
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']
        self.file = text_data_json.get('file')
        now = timezone.now()
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    async def save_message(self, event):
        user = await sync_to_async(User.objects.get)(username=event.get('user'))
     
        event['user'] = user
        event.pop('type')
        event['chatroom_id'] = self.id
        event['attachment'] = self.file
        message = await sync_to_async(Message.objects.create)(**event)
       


    async def chat_message(self, event,*args,**kwargs):
     
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))
        await self.save_message(event)
        






