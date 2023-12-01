from django.forms import ModelForm
from chat.entities.chat_rooms import ChatRoom
from chat.entities.message import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"