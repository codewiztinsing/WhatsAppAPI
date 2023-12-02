import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from chat.entities.message import Message
from chat.entities.chat_rooms import ChatRoom
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):


    # update count of rooom
    async def update_room_client_count(room_id, action):
        room = ChatRoom.objects.get(id=room_id)

        if action == 'add':
            room.active_clients += 1
        elif action == 'remove':
            room.active_clients -= 1

        room.save()

        return room.active_clients




    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chat_{self.id}'


        # Check client count before joining
        room = await sync_to_async(ChatRoom.objects.get)(id=self.id)
        if room.active_clients >= room.max_clients:
            await self.send_message({
                'type': 'error',
                'message': 'Room is full'
            })
            await self.close(code=403)  # Forbidden

        # Join room group and update client count
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,

        )
        await sync_to_async(update_room_client_count)(room_id=self.id, action='add')
    
        await self.accept()

    async def get_room_client_count(room_id):
        room = ChatRoom.objects.get(id=room_id)
        return room.active_clients


    async def disconnect(self, close_code):
        
        # Update client count on disconnect
        await sync_to_async(update_room_client_count)(room_id=self.id, action='remove')


        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

         # Broadcast room status update
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_status',
                'active_clients': await sync_to_async(get_room_client_count)(room_id=self.id)
            }
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
        






