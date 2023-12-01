from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from room.entities.message import Message


def create_message(request):
    rooms = None
    if request.method == 'POST':
        messages = Message.objects.create(request.POST)
       
    else:
        return render(request, 'chatroom/create.html',{'messages': messages})

