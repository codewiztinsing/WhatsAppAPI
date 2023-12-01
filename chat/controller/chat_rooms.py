from django.urls import path
from chat.services.room import chatroom_list,create_chatroom,chat_room


app_name = 'chat'


urlpatterns = [
path('room/<int:id>/', chat_room,
         name='chat_room'),

path('', chatroom_list,
         name='chatroom_list'),


path('create/', create_chatroom,
         name='create_chatroom'),
]
