from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .models import Room


# @login_required
def chat_room(request,id=None):
   try:
 # retrieve course with given id joined by the current user
      room = Room.objects.get(id=id)
   except Room.DoesNotExist:
 # user is not a student of the course or course does not exist
     return HttpResponseForbidden()
   return render(request, 'chat/room.html', {'room': room})
