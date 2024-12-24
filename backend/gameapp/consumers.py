import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class GameConsumer(WebsocketConsumer):
    HANDLERS = {
        "turn": 'turn_handler'
    }

    def connect(self):
        self.id = self.scope["url_route"]["kwargs"]["game_id"]
        self.room_group_name = f'game_{self.id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        print(f"Connected to game {self.id}")
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        info = text_data_json["info"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'turn_handler',
                'info': info
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def turn_handler(self, event):
        info = event['info']

        self.send(text_data=json.dumps({
            'type': 'turn',
            'info': info
        }))

class ShowActiveGamesConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'home'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'change_active_games_list_handler',
                "data": text_data_json
            }
        )

    def change_active_games_list_handler(self, event):
        data = event['data']

        self.send(text_data=json.dumps(data))


class SendGameRequestConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.room_group_name = f'user_{self.username}_waiting_request'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        sender_id = text_data_json["sender_id"]
        game_id = text_data_json["game_id"]
        print(sender_id, self.username)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_game_request_handler',
                'data': {
                    'sender_id': sender_id,
                    'recipient_id': self.username,
                    'game_id': game_id
                }
            }
        )

    def send_game_request_handler(self, event):
        data = event['data']

        self.send(text_data=json.dumps(data))