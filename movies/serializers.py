from django.db.models.aggregates import Avg
from rest_framework import serializers
from .models import Movie, Director, Actor, Genre
from community.models import Rating
from django.contrib.auth import get_user_model


class MovieListSerializer(serializers.ModelSerializer):

    # rate = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('title', 'id', 'poster_path', 'is_netflix', 'rating_average', 'release_date')

    # def get_rate(self, instance):
    #     return instance.rating_set.aggregate(rate=Avg('rating'))


class MovieDetailSerializer(serializers.ModelSerializer):

    class DirectorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Director
            fields = ('name', 'profile_path')

    class ActorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('name', 'profile_path')

    class RatingSerializer(serializers.ModelSerializer):
        class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = get_user_model()
                fields = ('id', 'username', 'nickname')
        
        user = UserSerializer(read_only=True)

        class Meta:
            model = Rating
            exclude = ('reported_users', 'movie')

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

    
    directors = DirectorSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    rate = serializers.SerializerMethodField()
    rating_set = RatingSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def get_rate(self, instance):
        return instance.rating_set.aggregate(rate=Avg('rating'))

class MovieSearchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'rating_average', 'poster_path')



class CelebSerializer(serializers.ModelSerializer):
    
    movies = MovieListSerializer(many=True, read_only=True)
    movies_count = serializers.IntegerField(
        source='movies.count',
        read_only=True
    )

    class Meta:
        model = Actor
        fields = '__all__'



class MovieRecommendedSerializer(serializers.ModelSerializer):

    # rate = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'







# class MovieListSerializer(serializers.ModelSerializer):

#     class DirectorSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Director
#             fields = ('name', 'profile_path')

#     class ActorSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Actor
#             fields = ('name', 'profile_path')
    
#     directors = DirectorSerializer(many=True, read_only=True)
#     actors = ActorSerializer(many=True, read_only=True)
#     rate = serializers.SerializerMethodField()

#     class Meta:
#         model = Movie
#         fields = '__all__'

#     def get_rate(self, instance):
#         return instance.rating_set.aggregate(rate=Avg('rating'))




# class MovieListSerializer(serializers.ModelSerializer):

#     rate = serializers.SerializerMethodField()

#     rate_avg = serializers.FloatField(
#         source='rating_set__rating.Avg',
#         read_only=True
#     )

#     class Meta:
#         model = Movie
#         fields = ('title', 'id', 'poster_path', 'is_netflix', 'rate', 'rate_avg')

#     def get_rate(self, instance):
#         return instance.rating_set.aggregate(rate=Avg('rating'))