from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        swappable = "AUTH_USER_MODEL"
