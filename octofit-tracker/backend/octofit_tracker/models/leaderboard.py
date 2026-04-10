from djongo import models

class Leaderboard(models.Model):
    team = models.CharField(max_length=50)
    points = models.IntegerField()
    rank = models.IntegerField()
    def __str__(self):
        return f"{self.team} - {self.rank}"
