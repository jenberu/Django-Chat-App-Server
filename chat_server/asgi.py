"""
ASGI config for chat_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from .middlewares import JWTAuthMiddleware
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_server.settings')

#e AuthMiddlewareStackclass provided by Channels supports standard Django authentication
django_asgi_app  = get_asgi_application()
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
 'http': django_asgi_app,
 'websocket':JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
})
