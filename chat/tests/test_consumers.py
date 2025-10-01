import pytest
import urllib.parse
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from convo_core.asgi import application
from chat.models import ChatRoom, Message
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_connect_and_message():
    user = await database_sync_to_async(User.objects.create_user)(
        username="alice", password="pass"
    )

    room_name = "testroom"
    token = str(RefreshToken.for_user(user).access_token)
    query = urllib.parse.urlencode({"token": token})

    communicator = WebsocketCommunicator(application, f"/ws/chat/{room_name}/?{query}")
    connected, _ = await communicator.connect()
    assert connected

    # Send a message
    await communicator.send_json_to({"message": "Hello World"})

    # Receive broadcast
    response = await communicator.receive_json_from()
    assert response["message"] == "Hello World"
    assert response["sender"] == user.username

    # Check in DB
    room = await database_sync_to_async(ChatRoom.objects.get)(name=room_name)
    msg = await database_sync_to_async(lambda: Message.objects.get(room=room))()
    msg_sender = await database_sync_to_async(lambda: msg.sender)()
    assert msg.content == "Hello World"
    assert msg_sender == user

    await communicator.disconnect()
