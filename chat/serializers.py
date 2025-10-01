from rest_framework import serializers
from .models import ChatRoom, Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # username instead of ID

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.StringRelatedField(many=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'participants', 'messages']
