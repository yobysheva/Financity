from django.db import models
from user.models import User

class Professions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    salary = models.FloatField()
    def __str__(self):
        return f"Profession {self.name} with salary {self.salary}"


class Player (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profession = models.ForeignKey(Professions, on_delete=models.CASCADE, null=True, blank=True, default=None)
    balance = models.FloatField(default=0)
    def __str__(self):
        return f"{self.user.username}`s player {self.id}"


class Game (models.Model):
    NG = "new game"
    ST = "started"
    FD = "finished"
    __UPDATE_STATUS = {
        NG: ST,
        ST: FD
    }
    STATUS_CHOICES = (
        (NG, "New game"),
        (ST, "Started"),
        (FD, "Finished"),
    )
    id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(Player, related_name='playersID')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=NG)
    def __str__(self):
        return f"gameID: {self.id} | status: {self.status}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Question(models.Model):
    QUESTION_TYPES = [
        (1, 'Развернутый'),
        (2, 'Варианты'),
    ]
    QUESTION_CATEGORIES = [
        (1, 'Государство'),
        (2, 'Развлечения'),
        (3, 'Недвижимость')
    ]
    id = models.AutoField(primary_key=True)
    category = models.IntegerField(choices=QUESTION_CATEGORIES)
    text = models.TextField()
    type = models.IntegerField(choices=QUESTION_TYPES)

    def __str__(self):
        return f"Question {self.id}: {self.text[:50]}"


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    sum_now = models.FloatField()
    sum_later = models.FloatField()
    period = models.IntegerField()
    scip = models.BooleanField(default=False)
    action_text = models.TextField()
    category = models.CharField(max_length=100, default="Ответ на вопрос")
    def __str__(self):
        return f"Answer {self.id} for Question {self.question.id}"


class Action(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='actions')
    sum = models.FloatField()
    period = models.IntegerField()
    scip = models.BooleanField(default=False)
    category = models.CharField(max_length=100, default="Действие")
    def __str__(self):
        return f"Action {self.id} by Player {self.player.id}"


class Chance(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    sum = models.FloatField()
    period = models.IntegerField()
    scip = models.BooleanField(default=False)
    category = models.CharField(max_length=100, default="Шанс")
    def __str__(self):
        return f"Chance {self.id} with action {self.text}"

