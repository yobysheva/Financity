import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing
import gameapp.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

print(chat.routing.websocket_urlpatterns + gameapp.routing.websocket_urlpatterns)

application = ProtocolTypeRouter({
	'http': get_asgi_application(),
	"websocket": AuthMiddlewareStack(
		URLRouter(
			chat.routing.websocket_urlpatterns + gameapp.routing.websocket_urlpatterns
		)
	),
})