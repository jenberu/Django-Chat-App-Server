from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            query_string = parse_qs(scope["query_string"].decode("utf-8"))
            token = query_string.get("token", [None])[0]
            if token is not None:
                validated_token = JWTAuthentication().get_validated_token(token)
                user = await database_sync_to_async(JWTAuthentication().get_user)(validated_token)
                scope["user"] = user
            else:
                scope["user"] = AnonymousUser()
        except (ValidationError, KeyError, TypeError):
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
