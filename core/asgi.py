import os

from channels.security.websocket import OriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import app.routing
from core.middleware.channels import JwtAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": OriginValidator(
        JwtAuthMiddlewareStack(
            URLRouter(
                app.routing.websocket_urlpatterns
            )
        ),
        ["*"]
    )
})
