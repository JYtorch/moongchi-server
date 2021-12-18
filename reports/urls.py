from . import views
from django.urls import path

app_name = 'reports'

urlpatterns = [
    # 모두 data가 없어도 됩니다! POST로 로그인되기만 하면...
    path('review/<int:review_id>/', views.review_report, name='review_report'),
    path('comment/<int:comment_id>/', views.comment_report, name='comment_report'),
    path('nestedcomment/<int:nestedcomment_id>/', views.nestedcomment_report, name='nestedcomment_report'),
    path('rating/<int:rating_id>/', views.rating_report, name='rating_report'),
]