from django.contrib.auth import get_user_model
from django.db.models import fields
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import serializers

from movies.models import Movie
from .models import Review, Comment, NestedComment, Rating


class ReviewListSerializer(serializers.ModelSerializer):

    # 해당 리뷰에 작성된 댓글을 위한 serializer
    class CommentSerializer(serializers.ModelSerializer):
        
        # 해당 댓글에 작성된 대댓글을 위한 serializer
        class NestedCommentSerializer(serializers.ModelSerializer):
            class UserSerializer(serializers.ModelSerializer):
                class Meta:
                    model = get_user_model()
                    fields = ('id', 'username', 'nickname')

            user = UserSerializer(read_only=True)
            
            class Meta:
                model = NestedComment
                fields = ('id', 'content', 'user', 'like_users', 'dlike_users', 'created_at')
        
        class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = get_user_model()
                fields = ('id', 'username', 'nickname')

        user = UserSerializer(read_only=True)

        nestedcomment_set = NestedCommentSerializer(many=True, read_only=True)
        
        class Meta:
            model = Comment
            fields = ('id', 'content', 'user', 'like_users', 'dlike_users', 'created_at', 
                'nestedcomment_set')

    # 해당 리뷰의 영화를 보여주기 위한 serializer
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('title', 'poster_path', 'id', 'release_date')


    # 해당 리뷰의 사용자를 보여주기 위한 serializer
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username', 'nickname')

    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    like_users_count = serializers.IntegerField(
        source='like_users.count',
        read_only=True
    )

    dlike_users_count = serializers.IntegerField(
        source='dlike_users.count',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'movie', 'user', 'title', 'content', 'updated_at', 'like_users', 
            'dlike_users', 'like_users_count', 'dlike_users_count', 'comment_set')


# title과 content만 이용하는 create용 serializer
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('reported_users', 'user', 'movie', 'like_users', 'dlike_users')


# content만 수정할 수 있는 update용 serializer
class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('reported_users', 'user', 'movie', 'like_users', 'dlike_users', 'title')


# 댓글 작성 시에 사용하는 serializer
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content')

# 대댓글 작성 시에 사용하는 serializer
class NestedCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NestedComment
        fields = ('id', 'content')




# 별점 작성 때 사용하는 serializer
class RatingSerializer(serializers.ModelSerializer):
    # rating = serializers.IntegerField(required=True)
    class Meta:
        model = Rating
        fields = ('rating', 'content')
        extra_kwargs = {'rating': {'required': True}}


# 추천순 리뷰 3개 보여줄 때 이용하는 serializer
class SidebarReviewSerializer(serializers.ModelSerializer):
    like_users_count = serializers.IntegerField(
        source='like_users.count',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'user', 'like_users_count')








# # 별점 리스트 보여줄 때 사용하는 serializer
# class RatingListSerializer(serializers.ModelSerializer):
#     like_users_count = serializers.IntegerField(
#         source='like_users.count',
#         read_only=True
#     )
#     dlike_users_count = serializers.IntegerField(
#         source='dlike_users.count',
#         read_only=True
#     )


#     class Meta:
#         model = Rating
#         exclude = ('reported_user',)