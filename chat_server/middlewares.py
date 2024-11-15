# middleware.py
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        token_name = b"sec-websocket-protocol"
        
        if token_name in headers:
            token = headers[token_name].decode().split(",")[0].strip()
            try:
                access_token = AccessToken(token)
                user = await database_sync_to_async(User.objects.get)(id=access_token["user_id"])
                scope["user"] = user
            except Exception:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()
            
        return await super().__call__(scope, receive, send)
