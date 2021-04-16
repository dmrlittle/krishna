import json, datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.custom import save,load

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username =  self.scope['user'].username
        dt = datetime.datetime.now()
        
        save(self.room_name, username, message, dt)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'dt': f"{dt.strftime('%I')}:{dt.strftime('%M')} {dt.strftime('%p')}",
                #'admin': '#ffff80' if self.scope['user'].groups.filter(name='miniadmin').exists() else ''
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        dt = event['dt']
        #admin = event['admin']


        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username':username,
            'dt':dt,
            #'admin':admin
            'sender': ['justify-content-end','msg1'] if self.scope['user'].username == username else []
        }))