from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

from django.dispatch.dispatcher import receiver

from chat.models import Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        group_name = self.scope['url_route']['kwargs']['chatroom']
        self.room_name = "group_%s"%group_name 

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)

        msg = Message(text = data['text'], sender_id= data['sender'], receiver_id = data['receiver'])
        msg.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type':'sendMessage',
                'text':data['text'],
                'sender':data['sender'],
                'receiver':data['receiver'],
                'timestamp':str(msg.timestamp),
            }
        )

    def sendMessage(self, event):
        msg = {'text':event['text'], 'sender': event['sender'], 'receiver': event['receiver'], 'timestamp' : event['timestamp']}
        self.send(json.dumps(msg))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name,
        )