from djongo import models
from series.models import Series
from review.models import Review

class Episode(models.Model):
    series=                     models.ForeignKey(Series, on_delete=models.CASCADE)
    episode_id=                 models.IntegerField()
    episode_name=               models.CharField(max_length=255)
    episode_length=             models.TimeField()
    episode_date=               models.DateField()
    episode_link=               models.URLField() #! Should use file field
    episode_rating=             models.IntegerField()
    review=                     models.ForeignKey(Review, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.episode_name