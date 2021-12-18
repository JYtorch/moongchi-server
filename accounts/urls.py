from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup),

    # 비밀번호를 변경합니다. 새 비밀번호와 비밀번호 확인이 필요합니다. 
    path('changepassword/', views.change_password, name='password_change'),

    # 사용자의 신고 내역을 보여줍니다.
    path('<str:username>/report-list/', views.report_list),

    # POST 메소드로 해당 유저를 follow(다시 선택하면 unfollow)합니다.
    path('<str:username>/follow/', views.follow, name='follow'),

    # 프로필 페이지를 위해 해당 유저의 팔로우, 팔로잉 수와 작성한 리뷰를 반환합니다.
    # 물론 본인이면 팔로우 기능은 안 됩니다...!
    path('<username>/', views.profile, name='profile'),

    # path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]