import os
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "convo_core.settings")

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

def get_application():
    from chat.middleware import JWTAuthMiddlewareStack
    import chat.routing

    return ProtocolTypeRouter({
        "http": django_asgi_app,
        "websocket": JWTAuthMiddlewareStack(
            URLRouter(chat.routing.websocket_urlpatterns)
        ),
    })

application = get_application()
