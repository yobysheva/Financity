from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
	re_path(r'ws/chat/', consumers.ChatConsumer.as_asgi()),
]

#(?P<room_name>\w+)