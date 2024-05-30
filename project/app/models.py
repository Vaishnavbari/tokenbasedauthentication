from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class user_registration(AbstractUser):
    email=models.EmailField(max_length=254,unique=True)
    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['username']