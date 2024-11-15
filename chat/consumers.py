import json
# from asgiref.sync import async_to_sync 
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Message
class ChatConsumer(AsyncWebsocketConsumer):
   async def connect(self):#called when new connection is recived
       self.user=self.scope['user']
       print(' self.user', self.user)

       # retrieves the room_id from the WebSocket connection’s UR
       self.id=self.scope['url_route']['kwargs']['room_id']
       self.room_group_name=f'chat_{self.id}'
       #add a new websocket connection to a group
       await self.channel_layer.group_add(self.room_group_name,self.channel_name)
       await self.accept()

   async def disconnect(self,close_code):
       # leave room group
      await self.channel_layer.group_discard(
                     self.room_group_name, self.channel_name
                      )
    
     # receive message from WebSocket
   async def receive(self, text_data=None, bytes_data=None):
         now=timezone.now()
        # json.loads() to load the received JSON data into a Python dictionary
         text_data_json=json.loads(text_data)
         message=text_data_json['message']

         #send message to a group
         await self.channel_layer.group_send(self.room_group_name,
                                                      {
                                                       'type':'chat_message',
                                                       'message':message  ,
                                                       'user':self.user.username,
                                                       'datetime':now.isoformat(),
                                                      }
                                                      )
         await self.persist_message(message)

   async def chat_message(self,event): 
        #send message to websocket 
        await self.send(text_data=json.dumps(event))    
   async def persist_message(self, message):
       # send message to WebSocket
       await Message.objects.acreate(
                user=self.user, room_id=self.id, content=message
               )      