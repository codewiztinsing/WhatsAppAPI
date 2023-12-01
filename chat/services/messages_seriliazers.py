from rest_framework import serializers
from chat.entities.message import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'user', 'message', 'attachment', 'datetime']
