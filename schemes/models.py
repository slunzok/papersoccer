from django.db import models

class KurnikReplay(models.Model):
    name = models.CharField(max_length=10)
    player1 = models.CharField(max_length=20)
    player2 = models.CharField(max_length=20)
    replay_date = models.CharField(max_length=10)
    replay_time = models.CharField(max_length=8)
    replay_round = models.CharField(max_length=3)
    player1_elo = models.CharField(max_length=4)
    player2_elo = models.CharField(max_length=4)
    moves = models.TextField(max_length=1000, blank=True)
    result = models.CharField(max_length=3)

    def __str__(self):
        return self.name
