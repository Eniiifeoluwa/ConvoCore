import json
import urllib.parse
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Decode room_name from URL
        raw_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_name = urllib.parse.unquote(raw_name)
        self.room_group_name = f"chat_{self.room_name}"

        # Authenticate user from query string token
        token = self._get_token_from_query()
        self.scope["user"] = await database_sync_to_async(self._get_user_from_token)(token)

        user = self.scope.get("user")
        if not user:
            await self.close()
            return

        # Create/get DB room and add participant
        self.room = await self.get_or_create_room(self.room_name)
        await self.add_participant(self.room, user)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        user = self.scope.get("user")
        if not message or not user:
            return

        msg = await self.save_message(self.room.name, user, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "sender": user.username,
                "sender_id": user.id,
                "timestamp": msg.timestamp.isoformat(),
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    # -----------------------
    # Helpers
    # -----------------------
    def _get_token_from_query(self):
        query_string = self.scope.get("query_string", b"").decode()
        qs = urllib.parse.parse_qs(query_string)
        return qs.get("token", [None])[0]

    def _get_user_from_token(self, token):
        if not token:
            return None
        try:
            # Lazy import
            from django.contrib.auth import get_user_model
            from rest_framework_simplejwt.tokens import UntypedToken
            from rest_framework_simplejwt.exceptions import TokenError
            from .models import ChatRoom, Message  # Lazy import

            User = get_user_model()
            validated_token = UntypedToken(token)
            user_id = validated_token["user_id"]
            return User.objects.get(id=user_id)
        except (TokenError, User.DoesNotExist):
            return None

    @database_sync_to_async
    def get_or_create_room(self, name):
        from .models import ChatRoom  # Lazy import
        room, _ = ChatRoom.objects.get_or_create(name=name)
        return room

    @database_sync_to_async
    def add_participant(self, room, user):
        room.participants.add(user)

    @database_sync_to_async
    def save_message(self, room_name, sender, content):
        from .models import Message, ChatRoom  # Lazy import
        room = ChatRoom.objects.get(name=room_name)
        return Message.objects.create(room=room, sender=sender, content=content)
