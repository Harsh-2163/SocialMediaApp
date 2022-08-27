from datetime import datetime
import uuid
import django
from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin


from django.utils.translation import gettext_lazy as _
# Create your models here.
from .managers import CustomUserManager
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'),unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='prof_obj')
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='post_obj')
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email

