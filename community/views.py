from django.db.models.aggregates import Count
from django.shortcuts import render
from .models import Review, Comment, NestedComment, Rating
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from .serializers import (ReviewListSerializer, ReviewCreateSerializer, ReviewUpdateSerializer, 
    CommentCreateSerializer, NestedCommentCreateSerializer, RatingSerializer, SidebarReviewSerializer)
from movies.serializers import MovieListSerializer
from movies.models import Movie
from django.db.models import Q



# Create your views here.

# 전체 리뷰 목록을 불러옵니다.
# @api_view(['GET'])
# def review_lists(request):
#     reviews = Review.objects.order_by('-pk')
#     serializer = ReviewListSerializer(reviews, many=True)
#     return Response(serializer.data)

# 전체 리뷰 목록을 페이지 별로 불러옵니다.
@api_view(['GET'])
def review_lists(request, page):
    try:
        reviews = Review.objects.order_by('-pk')[3 * (page - 1): 3 * page]
    except:
        reviews = Review.objects.order_by('-pk')[3 * page:]
        
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)

# 리뷰 상세 페이지를 불러옵니다.
@api_view(['GET'])
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    serializer = ReviewListSerializer(review)
    return Response(serializer.data)
    

# 영화 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if not request.user.like_movies.filter(pk=movie_id).exists():
        movie.like_users.add(request.user)
    else:
        movie.like_users.remove(request.user)

    if request.user.dlike_movies.filter(pk=movie_id).exists():
        movie.dlike_users.remove(request.user)
    
    return Response({'is_like': request.user.like_movies.filter(pk=movie_id).exists()}, status=status.HTTP_201_CREATED)


# 영화 싫어요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_dlike(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if not request.user.dlike_movies.filter(pk=movie_id).exists():
        movie.dlike_users.add(request.user)
    else:
        movie.dlike_users.remove(request.user)

    if request.user.like_movies.filter(pk=movie_id).exists():
        movie.like_users.remove(request.user)
    
    return Response({'is_dlike': request.user.dlike_movies.filter(pk=movie_id).exists()}, status=status.HTTP_201_CREATED)


# 리뷰 검색 기능입니다.
@api_view(['GET',])
def review_search(request, query):
    if query:
        reviews = Review.objects.filter(Q(title__icontains=query)|Q(content__icontains=query))
        serializer = ReviewListSerializer(reviews, many=True)
        if reviews:
            return Response(serializer.data)
        
    return Response({"message":"검색 결과가 없습니다ㅠ"}, status=status.HTTP_200_OK)

# 특정 영화의 리뷰 목록을 보여주거나 등록합니다
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_list_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    # print(movie.review_set.all().first().comment_set.all().first().nestedcomment_set.all())
    if request.method == 'GET':
        reviews = movie.review_set.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

    # 리뷰를 작성합니다. (title, content) 필요!
    elif request.method == 'POST':
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 특정 리뷰를 업데이트하거나 삭제합니다.
# content만 수정할 수 있음!
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_update_delete(request, movie_id, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if not request.user.review_set.filter(pk=review_id).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ReviewUpdateSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        return Response({ 'id': review_id }, status=status.HTTP_204_NO_CONTENT)

# 리뷰 좋아요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_like(request, movie_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if not request.user.like_reviews.filter(pk=review_id).exists():
        review.like_users.add(request.user)
    else:
        review.like_users.remove(request.user)

    if request.user.dlike_reviews.filter(pk=review_id).exists():
        review.dlike_users.remove(request.user)
    
    return Response({'is_like': request.user.like_reviews.filter(pk=review_id).exists()}, status=status.HTTP_201_CREATED)


# 리뷰 싫어요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_dlike(request, movie_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if not request.user.dlike_reviews.filter(pk=review_id).exists():
        review.dlike_users.add(request.user)
    else:
        review.dlike_users.remove(request.user)

    if request.user.like_reviews.filter(pk=review_id).exists():
        review.like_users.remove(request.user)
    
    return Response({'is_dlike': request.user.dlike_reviews.filter(pk=review_id).exists()}, status=status.HTTP_201_CREATED)



# 댓글 작성 기능
# content만 있으면 됩니다.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 댓글 삭제 기능.
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, review_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    # comment = Comment.objects.get(pk=comment_id)

    if not request.user.comment_set.filter(pk=comment_id).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({ 'id': comment_id }, status=status.HTTP_204_NO_CONTENT)


# 댓글 좋아요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_like(request, review_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if not request.user.like_comments.filter(pk=comment_id).exists():
        comment.like_users.add(request.user)
    else:
        comment.like_users.remove(request.user)

    if request.user.dlike_comments.filter(pk=comment_id).exists():
        comment.dlike_users.remove(request.user)
    
    return Response({'is_like': request.user.like_comments.filter(pk=comment_id).exists()}, status=status.HTTP_201_CREATED)


# 댓글 싫어요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_dlike(request, review_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if not request.user.dlike_comments.filter(pk=comment_id).exists():
        comment.dlike_users.add(request.user)
    else:
        comment.dlike_users.remove(request.user)

    if request.user.like_comments.filter(pk=comment_id).exists():
        comment.like_users.remove(request.user)
    
    return Response({'is_dlike': request.user.dlike_comments.filter(pk=comment_id).exists()}, status=status.HTTP_201_CREATED)


# 대댓글 작성 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nestedcomment_create(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    serializer = NestedCommentCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, comment=comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 대댓글 삭제 기능.
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def nestedcomment_delete(request, comment_id, nestedcomment_id):
    nestedcomment = get_object_or_404(NestedComment, pk=nestedcomment_id)

    if not request.user.nestedcomment_set.filter(pk=nestedcomment_id).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    nestedcomment.delete()
    return Response({ 'id': nestedcomment_id }, status=status.HTTP_204_NO_CONTENT)


# 대댓글 좋아요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nestedcomment_like(request, comment_id, nestedcomment_id):
    nestedcomment = get_object_or_404(NestedComment, pk=nestedcomment_id)
    if not request.user.like_nested_comments.filter(pk=nestedcomment_id).exists():
        nestedcomment.like_users.add(request.user)
    else:
        nestedcomment.like_users.remove(request.user)

    if request.user.dlike_nested_comments.filter(pk=nestedcomment_id).exists():
        nestedcomment.dlike_users.remove(request.user)
    
    return Response({'is_like': request.user.like_nested_comments.filter(pk=nestedcomment_id).exists()}, status=status.HTTP_201_CREATED)


# 대댓글 싫어요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nestedcomment_dlike(request, comment_id, nestedcomment_id):
    nestedcomment = get_object_or_404(NestedComment, pk=nestedcomment_id)
    if not request.user.dlike_nested_comments.filter(pk=nestedcomment_id).exists():
        nestedcomment.dlike_users.add(request.user)
    else:
        nestedcomment.dlike_users.remove(request.user)

    if request.user.like_nested_comments.filter(pk=nestedcomment_id).exists():
        nestedcomment.like_users.remove(request.user)
    
    return Response({'is_dlike': request.user.dlike_nested_comments.filter(pk=nestedcomment_id).exists()}, status=status.HTTP_201_CREATED)



# 해당 영화 별점 작성 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rating_list_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user.rating_set.filter(movie_id=movie_id).exists():
        return Response({'detail': '이미 작성된 한줄평이 있습니다.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = RatingSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        movie.rating_average = (movie.rating_average * (movie.rating_set.count() - 1) + serializer.data.get('rating', 8)) / movie.rating_set.count()
        movie.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 별점 삭제 기능.
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def rating_delete(request, movie_id, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)

    if not request.user.rating_set.filter(pk=rating_id).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    rating.delete()
    return Response({ 'id': rating_id }, status=status.HTTP_204_NO_CONTENT)


# 별점 좋아요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rating_like(request, movie_id, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if not request.user.like_ratings.filter(pk=rating_id).exists():
        rating.like_users.add(request.user)
    else:
        rating.like_users.remove(request.user)

    if request.user.dlike_ratings.filter(pk=rating_id).exists():
        rating.dlike_users.remove(request.user)
    
    return Response({'is_like': request.user.like_ratings.filter(pk=rating_id).exists()}, status=status.HTTP_201_CREATED)


# 별점 싫어요 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rating_dlike(request, movie_id, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if not request.user.dlike_ratings.filter(pk=rating_id).exists():
        rating.dlike_users.add(request.user)
    else:
        rating.dlike_users.remove(request.user)

    if request.user.like_ratings.filter(pk=rating_id).exists():
        rating.like_users.remove(request.user)
    
    return Response({'is_dlike': request.user.dlike_ratings.filter(pk=rating_id).exists()}, status=status.HTTP_201_CREATED)


# 사이드바에 들어갈 추천 많은 리뷰 3개를 반환합니다.
@api_view(['GET'])
def sidebar_reviews(request):
    reviews = Review.objects.annotate(like_count=Count('like_users')).order_by('-like_count')[:3]
    serializer = SidebarReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 사이드바에 들어갈 추천영화(한줄평이 많은 영화 중 평점이 높은 순서로)
@api_view(['GET'])
def sidebar_movies(request):
    popular_movies = Movie.objects.annotate(ratings_count=Count('rating')).order_by('-ratings_count')[:3]
    serializer = MovieListSerializer(popular_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)