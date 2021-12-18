from django.db import models
from django.conf import settings
from reports.models import ReviewReport, CommentReport, RatingReport, NestedCommentReport
from movies.models import Movie
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_reviews')
    dlike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dlike_reviews')
    updated_at = models.DateTimeField(auto_now=True)
    reported_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='reported_reviews',
        through=ReviewReport)


class Comment(models.Model):
    content = models.CharField(max_length=200)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_comments')
    dlike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dlike_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    reported_users = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        related_name='reported_comments', 
        through=CommentReport)


class NestedComment(models.Model):
    content = models.CharField(max_length=200)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_nested_comments')
    dlike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dlike_nested_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    reported_users = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        related_name='reported_nested_comments',
        through=NestedCommentReport)


class Rating(models.Model):
    rating = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    content = models.CharField(max_length=30)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_ratings')
    dlike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dlike_ratings')
    created_at = models.DateTimeField(auto_now_add=True)
    reported_users = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        related_name='reported_ratings',
        through=RatingReport)

    def __str__(self):
        return f'{self.rating}점, {self.content}'
