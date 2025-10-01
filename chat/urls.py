from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageCreateView, RoomMessagesView

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet, basename='room')
router.register(r'messages', MessageCreateView, basename='message')

urlpatterns = [
    path('', include(router.urls)),  # This creates /api/rooms/ and /api/messages/
    path('rooms/<str:room_name>/messages/', RoomMessagesView.as_view(), name='room-messages'),
]