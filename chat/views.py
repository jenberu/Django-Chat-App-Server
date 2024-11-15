from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .models import Room,Message
from rest_framework.views import APIView
from .serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework import status



# @login_required
def chat_room(request,id=None):
   try:
 # retrieve course with given id joined by the current user
      room = Room.objects.get(id=id)
   except Room.DoesNotExist:
 # user is not a student of the course or course does not exist
     return HttpResponseForbidden()
   latest_messages=room.chat_messages.select_related('user').order_by('-id')[:5]
   #reverse the message in chronological order
   latest_messages=reversed(latest_messages)
   return render(request, 'chat/room.html', {'room': room,'latest_messages': latest_messages})
class MessageViewset(APIView):
   def get(self,request,room_id):
      try:
          messages=Message.objects.filter(room__id=room_id)
          serializer=MessageSerializer(messages,many=True)
          return Response(serializer.data ,status=status.HTTP_200_OK)
      except Exception as e:
         return Response({
            'error':str(e)},
            status=status.HTTP_400_BAD_REQUEST
         )    

      
   
   
   
