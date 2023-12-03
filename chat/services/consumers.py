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
    def update_room_client_count(self,room_id, action):
        room = ChatRoom.objects.get(id=room_id)

        if action == 'add':
            room.active_client += 1
        elif action == 'remove':
            room.active_client -= 1

        room.save()

        return room.active_client


    def get_room_client_count(self,room_id):
        room = ChatRoom.objects.get(id=room_id)
        return room.active_client




    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        

        # Join room group and update client count
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,

        )


                # Check client count before joining
        room = await sync_to_async(ChatRoom.objects.get)(id=self.id)
        if room.active_client >= room.max_client:
        
         # Broadcast room status update
            await self.channel_layer.group_send(
              
            self.room_group_name,
            {
                'type': 'chat_error',
                'message': f"maxmium number of user reached or you are not loggedin",
                'user': self.user.username,
               
            }
            )
               # leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print(room.active_client,room.max_client,"room info")



        room_id = self.scope['url_route']['kwargs']['course_id']
        await sync_to_async(self.update_room_client_count)(room_id=room_id, action='add')
    
        await self.accept()




    async def disconnect(self, close_code):
        
        # Update client count on disconnect
        await sync_to_async(self.update_room_client_count)(room_id=self.id, action='remove')


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
                'active_clients': await sync_to_async(self.get_room_client_count)(room_id=self.id)
            }
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
 
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
        # if self.file:
        #     event['attachment'] = self.file
        message = await sync_to_async(Message.objects.create)(**event)
       


    async def chat_message(self, event,*args,**kwargs):


        # send message to WebSocket
        await self.send(text_data=json.dumps(event))
        await self.save_message(event)



    
    async def chat_error(self, event,*args,**kwargs):

        # send message to WebSocket
        await self.send(text_data=json.dumps(event))
    
        






