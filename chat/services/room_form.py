from django.forms import ModelForm
from chat.entities.chat_rooms import ChatRoom

class RoomForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = "__all__"