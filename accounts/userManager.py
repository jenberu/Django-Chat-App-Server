from django.http import Http404
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
class userManager(BaseUserManager):
    def get_user_by_id(self,user_id):
        try:
            instance=self.get(public_id=user_id)
            return instance
        except (ObjectDoesNotExist,ValueError,TypeError):
             raise ValueError("User with this public ID does not exist.")  
    def create_user(self,username=None,email=None,password=None,**kwargs):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise ValueError('Users must have a password.')
        user=self.model(username=username,email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username=None,email=None,password=None,**kwargs):
        user=self.create_user(username=username,password=password,email=email,**kwargs)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user

