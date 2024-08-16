from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    """
    User model representing a user in the system.
    Attributes:
        is_admin (bool): Indicates whether the user is an admin or not. Default is False.
    """    
    is_admin = models.BooleanField(default=False)
