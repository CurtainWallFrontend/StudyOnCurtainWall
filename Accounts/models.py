from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    access_system_a = models.BooleanField(default=False)
    access_system_b = models.BooleanField(default=False)
    access_system_c = models.BooleanField(default=False)
    access_system_d = models.BooleanField(default=False)
    access_system_e = models.BooleanField(default=False)
    access_system_f = models.BooleanField(default=False)