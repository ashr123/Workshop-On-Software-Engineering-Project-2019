from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class StoreOwnerConsumer(WebsocketConsumer):
    def connect(self):
        self.owner_id = self.scope['url_route']['kwargs']['owner_id']
        self.owner_group_name = 'owner_%s' % self.owner_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.owner_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.owner_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.owner_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))