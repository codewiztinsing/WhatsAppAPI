from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from chat.entities.chat_rooms import ChatRoom
from chat.entities.message import Message
from chat.services.room_form import RoomForm
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from chat.services.chat_rooms_seriliazers import ChatRoomSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def list(self, request):
        chat_rooms = self.get_queryset()
        serializer = self.get_serializer(chat_rooms, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        chat_room = self.get_object()
        serializer = self.get_serializer(chat_room)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        chat_room = self.get_object()
        serializer = self.get_serializer(chat_room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        chat_room = self.get_object()
        chat_room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#landing page for chat user
def chat_room(request,id):
   
    messages = None
    try:
        messages = Message.objects.filter(chatroom_id = id)
    except Message.DoesNotExist as e:
        print(e)
    return render(request, 'chat/room.html', {'id': id,'messages':messages})


# list of rooms avialable currently
def chatroom_list(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chat/home.html', {'chatrooms': chatrooms})


#create new chat room
def create_chatroom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        form.save()
        return redirect(reverse("chat:chatroom_list"))
       
    else:
        return render(request, 'chat/create.html',{'form': form})

# enter chat room
def enter_chatroom(request, chatroom_id):
    chatroom = get_object_or_404(Room, id=chatroom_id)
    messages = Message.objects.filter(chatroom=chatroom)
    return render(request, 'chatroom/chat.html', {'chatroom': chatroom, 'messages': messages})
