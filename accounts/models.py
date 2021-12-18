from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from movies.models import Movie
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    nickname_validator = UnicodeUsernameValidator()
    followings = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    nickname = models.CharField(
        max_length=30,
        unique=True,
        help_text= '필수 항목이며 중복은 불가능합니다. 글자, 숫자, @/./+/-/_만 사용 가능합니다.',
        validators=[nickname_validator],
        error_messages={
            'unique': "이미 해당 별명을 가진 사용자가 존재합니다.",
        },
    )
    def __str__(self): 
        return f'{self.username}, {self.nickname}'


class Playlist(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_playlists')
    dlike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dlike_playlists')
    
    def __str__(self): 
        return f'{self.title}, {self.movies}'