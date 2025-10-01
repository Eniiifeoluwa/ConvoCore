import pytest
from django.contrib.auth import get_user_model
from chat.models import ChatRoom, Message

User = get_user_model()


@pytest.mark.django_db
def test_chatroom_creation():
    room = ChatRoom.objects.create(name="Room1")
    assert room.name == "Room1"


@pytest.mark.django_db
def test_message_creation_and_ordering():
    user = User.objects.create_user(username="alice", password="pass")
    room = ChatRoom.objects.create(name="Room1")
    m1 = Message.objects.create(room=room, sender=user, content="Hi")
    m2 = Message.objects.create(room=room, sender=user, content="Hello again")

    messages = list(room.messages.all())
    assert messages[0] == m1
    assert messages[1] == m2


@pytest.mark.django_db
def test_participants_added_on_message():
    user = User.objects.create_user(username="bob", password="pass")
    room = ChatRoom.objects.create(name="Room2")

    Message.objects.create(room=room, sender=user, content="Hi there")

    room.refresh_from_db()
    assert user in room.participants.all()
