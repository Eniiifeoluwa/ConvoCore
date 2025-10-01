import urllib.parse
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser


class JWTAuthMiddleware(BaseMiddleware):
    """
    WebSocket middleware: authenticates user via JWT from header or query string
    """

    async def __call__(self, scope, receive, send):
        # Extract token from headers
        headers = dict(scope.get("headers", []))
        token = headers.get(b"sec-websocket-protocol", None)

        # If not in header, check query string
        if not token:
            query_string = scope.get("query_string", b"").decode()
            qs = urllib.parse.parse_qs(query_string)
            token = qs.get("token", [None])[0]

        # Get user from token (lazy database call)
        scope["user"] = await self.get_user(token)
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        if not token:
            return AnonymousUser()
        try:
            # Lazy imports here
            from django.contrib.auth import get_user_model
            from rest_framework_simplejwt.tokens import UntypedToken
            from rest_framework_simplejwt.exceptions import TokenError

            User = get_user_model()
            validated_token = UntypedToken(token)
            user_id = validated_token["user_id"]
            return User.objects.get(id=user_id)
        except (TokenError, User.DoesNotExist):
            return AnonymousUser()


def JWTAuthMiddlewareStack(inner):
    """Wrap JWT middleware with session support"""
    from channels.auth import AuthMiddlewareStack
    return AuthMiddlewareStack(JWTAuthMiddleware(inner))
