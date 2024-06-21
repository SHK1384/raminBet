from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Match)
def is_game_finished_changed(sender, instance=None, created=False, **kwargs):
    if not created and instance.is_finished and instance.team_1_score and instance.team_2_score:
        predictions = Prediction.objects.filter(match=instance)
        for prediction in predictions:
            user = prediction.user
            if prediction.team_1_score == instance.team_1_score and prediction.team_2_score == instance.team_2_score:
                user.score += 3
                user.save()
            elif abs(prediction.team_1_score - prediction.team_2_score) == abs(
                    instance.team_1_score - instance.team_2_score):
                user.score += 2
                user.save()
            elif (prediction.team_1_score > prediction.team_2_score and instance.team_1_score > instance.team_2_score) or (
                    prediction.team_2_score > prediction.team_1_score and instance.team_2_score > instance.team_1_score):
                user.score += 1
                user.save()

@receiver(post_save, sender=Team)
def is_finalist_champion_changed(sender, instance=None, created=False, **kwargs):
    if not created and instance.is_finalist:
        finalist_predictions = FinalistPrediction.objects.filter(team=instance)
        for prediction in finalist_predictions:
            user = prediction.user
            user.score += 10
            user.save()

    if not created and instance.is_champion:
        champion_predictions = ChampionPrediction.objects.filter(team=instance)
        for prediction in champion_predictions:
            user = prediction.user
            user.score += 20
            user.save()
