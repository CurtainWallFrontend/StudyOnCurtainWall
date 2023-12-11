from django.contrib.auth.backends import ModelBackend
from userAuthority.models import mydb

class CustomUserAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = mydb.objects.get(email=email)
            if user.check_password(password):
                return user
        except mydb.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return mydb.objects.get(pk=email)
        except mydb.DoesNotExist:
            return None
