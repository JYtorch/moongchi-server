from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User

from .serializers import UserSerializer, MyTokenObtainPairSerializer, UserReportListSerializer, UserProfileSerializer
import re

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
	# 1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
	# 1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
	# 2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
    
	# 3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다. (write_only)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# 해당 유저를 팔로우합니다.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, username):
    # 상대방
    target = get_object_or_404(get_user_model(), username=username)

    # 본인
    user = request.user
    if user == target:
        return Response({'message': '본인은 팔로우할 수 없어요ㅠ'}, status=status.HTTP_403_FORBIDDEN)
    else:
        if user.followings.filter(pk=target.pk).exists():
            user.followings.remove(target)
            return Response({'message': '언팔로우 하였습니다.'}, status=status.HTTP_201_CREATED)
        else:
            user.followings.add(target)
            return Response({'message': '팔로우 되었습니다.'}, status=status.HTTP_201_CREATED)
        

# 해당 유저의 프로필을 조회합니다.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)



# 사용자의 신고 내역을 보여줍니다.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_list(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    serializer = UserReportListSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def password_change(request):
#     print(request.user.password)
#     pwd = request.data.get('password')
#     encrypted_pwd = hashlib.sha256(pwd.encode()).hexdigest()
#     print('새 암호', encrypted_pwd)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):

	# 1-1. Client에서 온 데이터를 받아서
    password = request.data.get('newPassword')
    password_confirmation = request.data.get('newPasswordConfirmation')
		
	# 1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
	
    # 길이 체크
    if len(password) < 8 or len(password) > 30:
        return Response({'error': '비밀번호 길이가 너무 짧습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'username': request.user.username,
        'nickname': request.user.nickname,
        'password': password
    }

    serializer = UserSerializer(request.user, data=data)

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(password)
        user.save()

    return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_201_CREATED)
