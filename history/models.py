# External Import
from djongo import models

# Internal Import
from series.models import Series
from movie.models import Movie
from user.models import User


class History(models.Model):
    user =          models.ForeignKey(User, on_delete=models.CASCADE)
    series =        models.ForeignKey(Series, on_delete=models.CASCADE)
    movies=         models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.user