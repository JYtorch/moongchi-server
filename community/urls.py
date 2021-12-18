from . import views
from django.urls import path, include

app_name = 'community'

urlpatterns = [
    # 영화 전체 리뷰
    path('reviewlist/<int:page>/', views.review_lists, name='review_lists'),

    # 리뷰 상세 조회
    path('review/<int:review_id>/', views.review_detail, name='review_detail'),

    # 영화 좋아요, 싫어요
    path('<int:movie_id>/like/', views.movie_like, name='movie_like'),
    path('<int:movie_id>/dlike/', views.movie_dlike, name='movie_dlike'),

    # 해당 영화의 리뷰리스트, 작성
    # 리뷰 작성은 (title, content)만 넣어주면 됩니다.
    path('<int:movie_id>/review/', views.review_list_create, name='review_list_create'),

    # 리뷰 검색
    path('reviewsearch/<str:query>/', views.review_search, name='review_search'),

    # 리뷰 수정, 삭제, 좋아요, 싫어요
    # 리뷰 수정은 content만 가능하므로 content만 넣어주면 됩니다.
    path('<int:movie_id>/review/<int:review_id>/', views.review_update_delete, name='review_update_delete'),
    path('<int:movie_id>/review/<int:review_id>/like/', views.review_like, name='review_like'),
    path('<int:movie_id>/review/<int:review_id>/dlike/', views.review_dlike, name='review_dlike'),

    # 댓글 작성, 삭제, 좋아요, 싫어요
    # 댓글 작성은 content만 넣어주면 됩니다.
    path('<int:review_id>/comment/', views.comment_create, name='comment_create'),
    path('<int:review_id>/comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('<int:review_id>/comment/<int:comment_id>/like/', views.comment_like, name='comment_like'),
    path('<int:review_id>/comment/<int:comment_id>/dlike/', views.comment_dlike, name='comment_dlike'),

    # 대댓글 작성, 삭제, 좋아요, 싫어요
    path('<int:comment_id>/nestedcomment/', views.nestedcomment_create, name='nestedcomment_create'),
    path('<int:comment_id>/nestedcomment/<int:nestedcomment_id>/', views.nestedcomment_delete, name='nestedcomment_delete'),
    path('<int:comment_id>/nestedcomment/<int:nestedcomment_id>/like/', views.nestedcomment_like, name='nestedcomment_like'),
    path('<int:comment_id>/nestedcomment/<int:nestedcomment_id>/dlike/', views.nestedcomment_dlike, name='nestedcomment_dlike'),
    
    # 별점 작성
    # (rating, content)만 있으면 됩니다.
    path('<int:movie_id>/rating/', views.rating_list_create, name='rating_list_create'),
    # 별점 삭제, 좋아요, 싫어요
    path('<int:movie_id>/rating/<int:rating_id>/', views.rating_delete, name='rating_delete'),
    path('<int:movie_id>/rating/<int:rating_id>/like/', views.rating_like, name='rating_like'),
    path('<int:movie_id>/rating/<int:rating_id>/dlike/', views.rating_dlike, name='rating_dlike'),

    # 사이드바에 들어갈 리뷰 추천순 3개 반환
    path('sidebar-reviews/', views.sidebar_reviews, name='sidebar_reviews'),

    # 사이드바에 들어갈 영화 3개 반환
    path('sidebar-movies/', views.sidebar_movies, name='sidebar_movies'),
]