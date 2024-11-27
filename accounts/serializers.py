from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from .models import User
class UserSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(source='public_id',read_only=True, format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    class Meta:
       model = User
       fields = ['id', 'username', 'first_name',
                'last_name', 'email',
                'is_active', 'created', 'updated']
       read_only_fields = ['is_active']
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
        error_messages={
            "required": "Password is required.",
            "min_length": "Password must be at least 8 characters long.",
            "max_length": "Password cannot exceed 128 characters.",
        }
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password']

    def validate_email(self, value):
        """
        Custom validation for email field.
        Ensures no duplicate emails are registered.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        """
        Custom validation for username field.
        Ensures no duplicate usernames are registered.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        """
        Override the create method to hash the password.
        """
        return User.objects.create_user(**validated_data)
class LoginSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
      data=super().validate(attrs)#It uses the authenticate() django built in function
      refresh=self.get_token(self.user)
      data['user']=UserSerializer(self.user).data
      data['refresh']=str(refresh)
      data['access']=str(refresh.access_token)
      if api_settings.UPDATE_LAST_LOGIN:
         update_last_login(None,self.user)
  
      return data  
   