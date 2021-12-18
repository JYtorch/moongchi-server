from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reports.serializers import (ReviewReportSerializer, CommentReportSerializer, NestedCommentReportSerializer,
    RatingReportSerializer)

from community.serializers import ReviewListSerializer
from movies.serializers import MovieListSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'nickname', 'password',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['nickname'] = user.nickname

        return token


class UserReportListSerializer(serializers.ModelSerializer):
    
    review_reports = ReviewReportSerializer(many=True)
    comment_reports = CommentReportSerializer(many=True)
    nested_comment_reports = NestedCommentReportSerializer(many=True)
    rating_reports = RatingReportSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('review_reports', 'comment_reports', 'nested_comment_reports',
            'rating_reports')


# 프로필 페이지를 위해 팔로우, 팔로잉 수와 작성한 리뷰를 반환합니다.
class UserProfileSerializer(serializers.ModelSerializer):

    class FollowUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username', 'nickname')

    followings = FollowUserSerializer(many=True, read_only=True)
    followers = FollowUserSerializer(many=True, read_only=True)
    review_set = ReviewListSerializer(many=True, read_only=True)
    like_movies = MovieListSerializer(many=True, read_only=True)

    followers_count = serializers.IntegerField(
        source='followers.count',
        read_only=True
    )


    followings_count = serializers.IntegerField(
        source='followings.count',
        read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'followings', 'followers', 'review_set', 'followers_count', 
            'followings_count', 'like_movies')
