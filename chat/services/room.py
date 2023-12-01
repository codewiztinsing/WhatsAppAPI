from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from chat.entities.chat_rooms import ChatRoom
# from chat.entities.message import Message
from chat.services.room_form import RoomForm
from django.shortcuts import redirect
from django.urls import reverse


#landing page for chat user
def chat_room(request,id):
    return render(request, 'chat/room.html', {'id': id})


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
