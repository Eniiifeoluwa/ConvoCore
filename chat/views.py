from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

# Rooms & messages
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

class MessageCreateView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

# Fetch messages in a room
class RoomMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_name):
        try:
            room = ChatRoom.objects.get(name=room_name)
        except ChatRoom.DoesNotExist:
            return Response({"detail": "Room not found."}, status=404)
        messages = Message.objects.filter(room=room).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
