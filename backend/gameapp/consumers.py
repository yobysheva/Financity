import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from gameapp.models import Player, Professions


class GameConsumer(WebsocketConsumer):
    HANDLERS = {
        "turn": 'turn_handler'
    }

    def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.player_id = self.scope["url_route"]["kwargs"]["player_id"]
        self.room_group_name = f'game_{self.game_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        profession = Professions.objects.order_by('?').first()
        player = Player.objects.get(id=self.player_id)
        player.profession = profession
        player.save()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notification_about_connect_to_game_handler',
                'info': {
                    'player_id': player.id,
                    'profession': player.profession.name,
                    'balance': player.balance,
                    'salary': player.profession.salary
                }
            }
        )

        print(f"Connected to game {self.game_id}")
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        info = text_data_json
        print(info)
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
            'info': info
        }))

    def notification_about_connect_to_game_handler(self, event):
        info = event['info']

        self.send(text_data=json.dumps({
            'info': {
                "info": info,
                "type": 'notification_about_connect_to_game'
            }
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

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def change_active_games_list_handler(self, event):
        data = event['data']

        self.send(text_data=json.dumps(data))


# class SendGameRequestConsumer(WebsocketConsumer):
#     def connect(self):
#         self.username = self.scope["url_route"]["kwargs"]["username"]
#         self.room_group_name = f'user_{self.username}_waiting_request'
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         self.accept()
#
#     def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         sender_id = text_data_json["sender_id"]
#         game_id = text_data_json["game_id"]
#         print(sender_id, self.username)
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'send_game_request_handler',
#                 'data': {
#                     'sender_id': sender_id,
#                     'recipient_id': self.username,
#                     'game_id': game_id
#                 }
#             }
#         )
#
#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
#
#     def send_game_request_handler(self, event):
#         data = event['data']
#
#         self.send(text_data=json.dumps(data))

class SendGameRequestConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.room_group_name = f'waiting_request_{self.username}'
        print("CONNECT " + self.username)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        sender_id = text_data_json['sender_id']
        game_id = text_data_json['game_id']
        print(f"Received data: sender_id={sender_id}, game_id={game_id}")

        # Отправляем сообщение в группу
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_game_invitation',
                'sender_id': sender_id,
                'game_id': game_id
            }
        )

    # Обработчик для отправки данных клиенту
    def send_game_invitation(self, event):
        sender_id = event['sender_id']
        game_id = event['game_id']

        self.send(text_data=json.dumps({
            'type': 'game_invitation',
            'sender_id': sender_id,
            'game_id': game_id
        }))
