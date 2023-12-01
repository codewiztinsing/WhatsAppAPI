from rest_framework import serializers
from chat.entities.chat_rooms import ChatRoom

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'description', 'created_at']
