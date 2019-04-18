from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    image = models.ImageField(blank=True, default="default_image.png")
    
    def __str__(self):
        return str(self.user) + '('+ self.nickname + ')' + '님은' + self.description
        

class User(AbstractUser):
    follows = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followings", blank=True)