from django.db import models

from chat_server.settings import AUTH_USER_MODEL
class Room(models.Model):
    name=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
    

class Message(models.Model):
    room = models.ForeignKey(Room, related_name="chat_messages", on_delete=models.PROTECT)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='chat_message')
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
         return f'{self.user} on {self.room} at {self.sent_on}'




