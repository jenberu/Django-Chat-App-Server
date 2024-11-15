from rest_framework import serializers
from . models import Message
from accounts.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()# Displays the string representation of the user
    room=serializers.StringRelatedField()

    class Meta:
        model=Message
        fields = ['id', 'room', 'user', 'content', 'sent_on']
