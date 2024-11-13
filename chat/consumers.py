import json
from channels.generic.websocket import WebsocketConsumer
class ChatConsumer(WebsocketConsumer):
    def connect(self):#called when new connection is recived
       self.accept()

    def disconnect(self,close_code):
           
           pass
     # receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # json.loads() to load the received JSON data into a Python dictionary
         text_data_json=json.loads(text_data)
         message=text_data_json['message']
         #send message to ebsocket ransforming it into JSON format again through json.dumps().
         self.send(text_data=json.dumps({'message':message}))