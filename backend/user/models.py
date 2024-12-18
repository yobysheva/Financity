from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    countGames = models.IntegerField(default=0)
    winGames = models.IntegerField(default=0)
