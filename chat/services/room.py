from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from chat.services.chat_rooms_seriliazers import ChatRoomSerializer
from chat.entities.chat_rooms import ChatRoom

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
