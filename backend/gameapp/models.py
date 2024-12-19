from django.db import models
from user.models import User


class Player (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}`s player {self.id}"


class Game (models.Model):
    id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(Player, related_name='playersID')
    status = models.CharField(max_length=50)
    def __str__(self):
        return f"gameID: {self.id} | status: {self.status}"

