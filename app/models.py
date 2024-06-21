from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=50)
    is_finalist = models.BooleanField(default=False)
    is_champion = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Match(models.Model):
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_1_Match')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_2_Match')
    team_1_score = models.IntegerField(null=True, blank=True)
    team_2_score = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.team_1.name + ' vs ' + self.team_2.name

class Prediction(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match_predictions')
    team_1_score = models.IntegerField()
    team_2_score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FinalistPrediction(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ChampionPrediction(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

