from django.urls import path
from . import views
app_name='chat'
urlpatterns = [
 path('room/<int:id>', views.chat_room, name='chat_room'),
 path('messages/<int:room_id>/',views.MessageViewset.as_view(),name='message'),
]