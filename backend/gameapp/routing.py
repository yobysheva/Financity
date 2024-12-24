from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<game_id>\d+)/(?P<player_id>\d+)/$', consumers.GameConsumer.as_asgi()),
    re_path(r'ws/home/', consumers.ShowActiveGamesConsumer.as_asgi()),
    re_path(r'ws/waiting_request/(?P<username>\w+)/$', consumers.SendGameRequestConsumer.as_asgi()),
    re_path(r'ws/for_waiting_request/(?P<username>\w+)/$', consumers.SendGameRequestConsumer.as_asgi()),
]
