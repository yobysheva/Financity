import string
import random

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    countGames = models.IntegerField(default=0)
    winGames = models.IntegerField(default=0)
    indexPhoto = models.IntegerField(default=0)
    secret = models.CharField(max_length=50, default=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)))