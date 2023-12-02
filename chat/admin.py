from django.contrib import admin
from chat.entities.chat_rooms import ChatRoom
from chat.entities.message import Message



admin.site.register(ChatRoom)
admin.site.register(Message)

