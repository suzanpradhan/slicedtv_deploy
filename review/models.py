# #External Import
from djongo import models

# Internal Import
from user.models import User


class Review(models.Model):
    review_id=                  models.IntegerField()
    review_title=               models.CharField(max_length=255)
    description=                models.CharField(max_length=255)
    user=                       models.ForeignKey(User, on_delete=models.CASCADE)
    date=                       models.DateTimeField()
    rating=                     models.FloatField()
    
    def __str__(self):
        return self.review_title
