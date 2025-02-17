import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(WebsocketConsumer):
	room_group_name = 'test'

	def connect(self):
		self.room_id = self.scope['url_route']['kwargs']['room_id']
		self.room_group_name = f'test_{self.room_id}'

		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		print("trying to connect")
		self.accept()
		print("accepted")

	def receive(self, text_data=None, bytes_data=None):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name, {
				'type': 'chat_message',
				'message': message,
				'username': username,
			}
		)

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

	def chat_message(self, event):
		message = event['message']
		username = event['username']

		self.send(text_data=json.dumps({
			'message': message,
			'username': username
		}))
