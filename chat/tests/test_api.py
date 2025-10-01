import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from chat.models import ChatRoom, Message

User = get_user_model()


@pytest.mark.django_db
def test_room_list():
    client = APIClient()
    user = User.objects.create_user(username="alice", password="pass")
    client.force_authenticate(user=user)

    # Create a room manually (no auto-create on search in current view)
    room = ChatRoom.objects.create(name="NewRoom")
    room.participants.add(user)

    res = client.get("/api/chat/rooms/")
    assert res.status_code == 200
    room_names = [r["name"] for r in res.data]
    assert "NewRoom" in room_names
