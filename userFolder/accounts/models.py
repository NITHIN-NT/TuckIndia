from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    profile = models.ImageField(upload_to='Profile', height_field=None, width_field=None, max_length=None)
    