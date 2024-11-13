import json
from asgiref.sync import async_to_sync 
from channels.generic.websocket import WebsocketConsumer
class ChatConsumer(WebsocketConsumer):
    def connect(self):#called when new connection is recived
       # retrieves the room_id from the WebSocket connection’s UR
       self.id=self.scope['url_route']['kwargs']['room_id']
       self.room_group_name=f'chat_{self.id}'
       #add a new websocket connection to a group
       async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
       self.accept()

    def disconnect(self,close_code):
       # leave room group
       async_to_sync(self.channel_layer.group_discard)(
                     self.room_group_name, self.channel_name
                      )
    
     # receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # json.loads() to load the received JSON data into a Python dictionary
         text_data_json=json.loads(text_data)
         message=text_data_json['message']
         print('message',message)
         #send message to websocket ransforming it into JSON format again through json.dumps().
         self.send(text_data=json.dumps({'message':message}))