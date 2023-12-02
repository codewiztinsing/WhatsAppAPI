from rest_framework import viewsets, status
from rest_framework.response import Response
from chat.services.messages_seriliazers import MessageSerializer
from chat.entities.message import Message
from django.contrib.auth.models import User


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]

    def list(self, request):
        if request.user.is_authenticated:
            chatroom_id = request.GET.get('chatroom')
            if chatroom_id is not None:
                queryset = self.get_queryset().filter(chatroom=chatroom_id)
            else:
                queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Unauthorized'})

    def create(self, request):
        if request.user.is_authenticated:
            chatroom = ChatRoom.objects.get(id=request.data['chatroom'])
            user = User.objects.get(id=request.user.id)
            message = Message(chatroom=chatroom, user=user, message=request.data['message'])
            message.save()
            serializer = self.get_serializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Unauthorized'})

    def retrieve(self, request, pk):
        if request.user.is_authenticated:
            message = self.get_object()
            serializer = self.get_serializer(message)
            return Response(serializer.data)
        else:
            return Response({'error': 'Unauthorized'})

    def update(self, request, pk):
        if request.user.is_authenticated:
            message = self.get_object()
            message.message = request.data['message']
            message.save()
            serializer = self.get_serializer(message)
            return Response(serializer.data)
        else:
            return Response({'error': 'Unauthorized'})

    def destroy(self, request, pk):
        if request.user.is_authenticated:
            message = self.get_object()
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Unauthorized'})
