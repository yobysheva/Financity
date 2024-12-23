import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(WebsocketConsumer):
	room_group_name = 'test'

	def connect(self):
		self.room_group_name = 'test'

		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		print("trying to connect")
		self.accept()
		print("accepted")

		print(self.groups)

	def receive(self, text_data=None, bytes_data=None):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]

		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name, {
				'type': 'chat_message',
				'message': message
			}
		)

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

	def chat_message(self, event):
		message = event['message']

		self.send(text_data=json.dumps({
			'message': message
		}))
