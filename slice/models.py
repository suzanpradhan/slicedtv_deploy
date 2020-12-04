# External Import
from djongo import models

# Internal Import
from user.models import User

class Cast(models.Model):
    cast_name =      models.CharField(max_length=200)
    cast_img =  models.ImageField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.cast

class Gallery(models.Model):
    image = models.ImageField()

    def __str__(self):
        return self.image


class Genre(models.Model):
    genre = models.CharField(max_length=200)

    def __str__(self):
        return self.genre

class Language(models.Model):
    language = models.CharField(max_length=200)

    def __str__(self):
        return self.language
