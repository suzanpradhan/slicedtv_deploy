# External Import
from djongo import models

# Internal Import
from slice.models import Cast, Language, Genre, Gallery

class Movie(models.Model):
    movie_name=                models.CharField(max_length=255)
    movie_poster=              models.URLField() #! Should use image field
    genre=                     models.ManyToManyField(Genre)    
    description=               models.CharField(max_length=255)
    trailer_link=              models.URLField() #! Should use File filed
    movie_link=                models.URLField() #! Should use File field
    movie_length=              models.TimeField()
    cast=                      models.ArrayField(model_container=Cast) #? Don't now if array field work for image.
    language=                  models.ManyToManyField(Language)
    aired=                     models.DateField()
    review_ID=                 models.IntegerField()
    rating_info=               models.FloatField()
    production_Company=        models.CharField(max_length=255)
    gallery=                   models.ManyToManyField(Gallery)


    objects = models.DjongoManager()
    
    def __str__(self):
        return self.movie_name