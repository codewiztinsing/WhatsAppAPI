from django.urls import path
# from chat.services.room import chatroom_list,create_chatroom,chat_room
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.services.message  import MessageViewSet

# app_name = 'chat'
router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
