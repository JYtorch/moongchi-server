from django.db.models.aggregates import Avg
from rest_framework import serializers
from .models import ReviewReport, CommentReport, NestedCommentReport, RatingReport
from community.models import Review, Comment, NestedComment, Rating
from django.contrib.auth import get_user_model

class ReviewReportSerializer(serializers.ModelSerializer):
    class ReviewContentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('id','content',)

    review = ReviewContentSerializer(read_only=True)

    class Meta:
        model = ReviewReport
        fields = ('review', 'created_at')


class CommentReportSerializer(serializers.ModelSerializer):
    class CommentContentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content',)

    comment = CommentContentSerializer(read_only=True)
    # serializers.DateTimeField

    class Meta:
        model = CommentReport
        fields = ('comment', 'created_at')


class NestedCommentReportSerializer(serializers.ModelSerializer):
    class NestedCommentContentSerializer(serializers.ModelSerializer):
        class Meta:
            model = NestedComment
            fields = ('id', 'content',)

    nestedcomment = NestedCommentContentSerializer(read_only=True)
    class Meta:
        model = NestedCommentReport
        fields = ('nestedcomment', 'created_at')


class RatingReportSerializer(serializers.ModelSerializer):
    class RatingContentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rating
            fields = ('id', 'content',)

    rating = RatingContentSerializer(read_only=True)
    class Meta:
        model = RatingReport
        fields = ('rating', 'created_at')
