from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .managers import CustomUserManager
class CustomUser(AbstractUser):
   username = None
   full_name = models.CharField(max_length=100)
   bio = models.TextField(blank=True)
   profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
   email = models.EmailField(_('email address'),unique=True)
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = []
   objects = CustomUserManager()

   def __str__(self):
        return self.email
   


