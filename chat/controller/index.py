from django.urls import path
# from chat.services.room import chatroom_list,create_chatroom,chat_room
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.services.message  import MessageViewSet
from chat.services.room  import ChatRoomViewSet
from .routing import websocket_urlpatterns


# app_name = 'chat'
router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'chat-rooms', ChatRoomViewSet, basename='chat-rooms')


urlpatterns = [
    path('', include(router.urls))
  
]
