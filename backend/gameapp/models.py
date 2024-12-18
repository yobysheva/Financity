from django.db import models
from user.models import User


class Player (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Game (models.Model):
    id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(Player, related_name='playersID')
    status = models.CharField(max_length=50)

