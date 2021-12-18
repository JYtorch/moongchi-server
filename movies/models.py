from django.db import models
from django.conf import settings



# Create your models here.
class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_movies')
    dlike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dlike_movies')
    genres = models.ManyToManyField(Genre, related_name='movies')
    overview = models.TextField()
    poster_path = models.CharField(max_length=200, default='', null=True, blank=True)
    video_path = models.CharField(max_length=200, default='', blank=True, null=True)
    release_date = models.DateField(blank=True, default='0001-01-01')
    country = models.CharField(max_length=70, blank=True, null=True)
    popularity = models.FloatField()
    is_netflix = models.BooleanField(default=False)
    rating_average = models.FloatField(blank=True)

    def __str__(self):
        return f'{self.title}, {len(self.overview)}'


class Director(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    profile_path = models.CharField(max_length=200, blank=True, null=True, default='')
    movies = models.ManyToManyField(Movie, related_name='director') # 작품들

    def __str__(self):
        return self.name


class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    profile_path = models.CharField(max_length=200, blank=True, null=True, default='')
    movies = models.ManyToManyField(Movie, related_name='actors')
    def __str__(self):
        return self.name