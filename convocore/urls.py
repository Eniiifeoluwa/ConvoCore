from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.views import ChatRoomViewSet, MessageCreateView

router = DefaultRouter()
router.register('rooms', ChatRoomViewSet)
router.register('messages', MessageCreateView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),  # user registration/login
    path('api/chat/', include(router.urls)),   # rooms & messages
    path('api/chat/', include('chat.urls')),   # room messages
]
