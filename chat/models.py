from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_group = models.BooleanField(default=False)
    participants = models.ManyToManyField(User, related_name='chatrooms', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Room {self.id}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)

    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        """
        Save message and ensure sender is added as a participant of the room.
        This keeps participants in sync when a user sends a message.
        """
        super().save(*args, **kwargs)
        # Add sender to participants (idempotent)
        self.room.participants.add(self.sender)

    def __str__(self):
        return f"{self.sender} in {self.room}: {self.content[:20]}"
