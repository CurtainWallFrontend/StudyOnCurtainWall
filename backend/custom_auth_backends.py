from django.contrib.auth.backends import ModelBackend
from userAuthority.models import SEUser

class CustomUserAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = SEUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except SEUser.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return SEUser.objects.get(pk=email)
        except SEUser.DoesNotExist:
            return None
