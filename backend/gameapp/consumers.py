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
        player = Player.objects.get(id=self.player_id)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notification_about_connect_to_game_handler',
                'info': {
                    'id': player.id,
                    'name': player.user.username,
                    'profession': player.profession.name,
                    'balance': player.balance,
                    'salary': player.profession.salary
                }
            }
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        info = text_data_json
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


class SendGameRequestConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.room_group_name = f'waiting_request_{self.username}'
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
        sender = text_data_json['sender']
        game_id = text_data_json['game_id']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_game_invitation',
                'sender': sender,
                'game_id': game_id
            }
        )

    def send_game_invitation(self, event):
        sender = event['sender']
        game_id = event['game_id']

        self.send(text_data=json.dumps({
            'type': 'game_invitation',
            'sender': sender,
            'game_id': game_id
        }))


class QuestionConsumer(WebsocketConsumer):
    def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.room_group_name = f'question_{self.game_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        type_ = text_data_json['type']
        match type_:
            case "textAnswer":
                text = text_data_json['text']

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'default_handler',
                        'info': {
                            'type': 'change_text_answer',
                            'content': {
                                'text': text,
                            },
                        }
                    }
                )
            case "radioButtonAnswer":
                buttonId = text_data_json['button_id']

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'default_handler',
                        'info': {
                            'type': 'radio_button_answer',
                            'content': {
                                'button_id': buttonId,
                            },
                        }
                    }
                )

            case 'vote':
                vote = text_data_json['vote']
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'default_handler',
                        'info': {
                            'type': 'vote',
                            'content': {
                                'vote': vote
                            }
                        }
                    }
                )

    def  default_handler(self, event):
        info = event['info']

        self.send(text_data=json.dumps({
            'info': info
        }))