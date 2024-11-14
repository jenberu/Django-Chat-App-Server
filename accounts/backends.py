from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if the username is an email or a username
        User = get_user_model()
        try:
            # Check if username is an email or a standard username
            user = User.objects.get(email=username) if '@' in username else User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

       
