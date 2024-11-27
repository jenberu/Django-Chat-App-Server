import uuid
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from .userManager import UserManager
class User(AbstractBaseUser, PermissionsMixin):
   public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
   username = models.CharField(db_index=True,max_length=255, unique=True)
   first_name = models.CharField(max_length=255)
   last_name = models.CharField(max_length=255)

   email=models.EmailField(db_index=True,unique=True,)
#    bio = models.TextField(blank=True, null=True)  # Optional bio field (text)
#    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
   is_active=models.BooleanField(default=True)
   is_staff=models.BooleanField(default=False)
   created=models.DateTimeField(auto_now_add=True)
   updated=models.DateTimeField(auto_now=True)
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']
   objects=UserManager()
   def __str__(self):
       return f"{self.username}"
   @property
   def name(self):
       return f"{self.first_name} {self.last_name}"