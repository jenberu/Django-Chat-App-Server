from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
import aiohttp
import asyncio

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            # Parse query string parameters
            query_string = parse_qs(scope["query_string"].decode("utf-8"))

            token = query_string.get("token", [None])[0]
            refresh_token = query_string.get("refresh_token", [None])[0]

            if token:
                try:
                    # Validate the token
                    validated_token = JWTAuthentication().get_validated_token(token)
                    user = await database_sync_to_async(JWTAuthentication().get_user)(validated_token)
                    scope["user"] = user
                except (InvalidToken, TokenError):
                    if refresh_token:
                        # Try to refresh the access token
                        new_access_token = await self.refresh_access_token(refresh_token)
                        if new_access_token:
                            validated_token = JWTAuthentication().get_validated_token(new_access_token)
                            user = await database_sync_to_async(JWTAuthentication().get_user)(validated_token)
                            scope["user"] = user
                        else:
                            scope["user"] = AnonymousUser()
                    else:
                        scope["user"] = AnonymousUser()
            else:
                scope["user"] = AnonymousUser()
        except (KeyError, ValueError, TypeError):
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    async def refresh_access_token(self, refresh_token):
        try:
            # Define the refresh token URL
            refresh_url = "http://localhost:8000/accounts/token/refresh/"
            async with aiohttp.ClientSession() as session:
                async with session.post(refresh_url, json={"refresh": refresh_token}) as response:
                    if response.status == 200:
                        # Parse JSON response for the new access token
                        response_data = await response.json()
                        return response_data.get("access")
                    else:
                        print(f"Failed to refresh token: {response.status}")
                        return None
        except Exception as e:
            print(f"Error refreshing token: {str(e)}")
            return None
