from django.shortcuts import render
from .serializers import (ReviewReportSerializer, CommentReportSerializer, NestedCommentReportSerializer,
    RatingReportSerializer)
from .models import ReviewReport, CommentReport, NestedCommentReport, RatingReport
from community.models import Review, Comment, NestedComment, Rating
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404

# Create your views here.

# 리뷰를 신고합니다.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_report(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user.reported_reviews.filter(pk=review_id).exists():
        return Response({'detail': '이미 신고한 리뷰입니다.', 
            '현재 신고된 횟수': review.reported_users.count()}, status=status.HTTP_403_FORBIDDEN)
    serializer = ReviewReportSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(author=request.user, review=review)
        if review.reported_users.count() >= 10:
            review.delete()
            return Response({'detail': '신고된 횟수가 10번이 넘어 게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# 댓글을 신고합니다.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_report(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user.reported_comments.filter(pk=comment_id).exists():
        return Response({'detail': '이미 신고한 댓글입니다.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommentReportSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(author=request.user, comment=comment)
        if comment.reported_users.count() >= 10:
            comment.delete()
            return Response({'detail': '신고된 횟수가 10번이 넘어 게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 대댓글을 신고합니다.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nestedcomment_report(request, nestedcomment_id):
    nestedcomment = get_object_or_404(NestedComment, pk=nestedcomment_id)
    if request.user.reported_nested_comments.filter(pk=nestedcomment_id).exists():
        return Response({'detail': '이미 신고한 댓글입니다.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = NestedCommentReportSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(author=request.user, nestedcomment=nestedcomment)
        if nestedcomment.reported_users.count() >= 10:
            nestedcomment.delete()
            return Response({'detail': '신고된 횟수가 10번이 넘어 게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 한줄평을 신고합니다.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rating_report(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if request.user.reported_ratings.filter(pk=rating_id).exists():
        return Response({'detail': '이미 신고한 한줄평입니다.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = RatingReportSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(author=request.user, rating=rating)
        if rating.reported_users.count() >= 10:
            rating.delete()
            return Response({'detail': '신고된 횟수가 10번이 넘어 게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
















# # 리뷰를 신고합니다.
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def review_report(request, review_id):
#     review = get_object_or_404(Review, pk=review_id)
#     if request.user.reported_reviews.filter(pk=review_id).exists():
#         return Response({'detail': '이미 신고한 리뷰입니다.', 
#             '현재 신고된 횟수': review.reported_users.count()}, status=status.HTTP_403_FORBIDDEN)
#     serializer = ReviewReportSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(author=request.user, review=review)
#         if review.reported_users.count() >= 10:
#             review.delete()
#             return Response({'detail': '신고된 횟수가 10번이 넘어 게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)



# # 댓글을 신고합니다.
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def comment_report(request, comment_id):
#     comment = get_object_or_404(Comment, pk=comment_id)
#     if request.user.reported_comments.filter(pk=comment_id).exists():
#         return Response({'detail': '이미 신고한 댓글입니다.'}, status=status.HTTP_403_FORBIDDEN)
#     serializer = CommentReportSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(author=request.user, comment=comment)
#         if comment.reported_users.count() >= 10:
#             comment.delete()
#             return Response({'detail': '신고된 횟수가 10번이 넘어 게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# # 대댓글을 신고합니다.
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def nestedcomment_report(request, nestedcomment_id):
#     nestedcomment = get_object_or_404(NestedComment, pk=nestedcomment_id)
#     if request.user.reported_nested_comments.filter(pk=nestedcomment_id).exists():
#         return Response({'detail': '이미 신고한 댓글입니다.'}, status=status.HTTP_403_FORBIDDEN)
#     serializer = NestedCommentReportSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(author=request.user, nestedcomment=nestedcomment)
#         if nestedcomment.reported_users.count() >= 10:
#             nestedcomment.delete()
#             return Response({'detail': '신고된 횟수가 10번이 넘어 게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# # 한줄평을 신고합니다.
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def rating_report(request, rating_id):
#     rating = get_object_or_404(Rating, pk=rating_id)
#     if request.user.reported_ratings.filter(pk=rating_id).exists():
#         return Response({'detail': '이미 신고한 한줄평입니다.'}, status=status.HTTP_403_FORBIDDEN)
#     serializer = RatingReportSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(author=request.user, rating=rating)
#         if rating.reported_users.count() >= 10:
#             rating.delete()
#             return Response({'detail': '신고된 횟수가 10번이 넘어 게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)