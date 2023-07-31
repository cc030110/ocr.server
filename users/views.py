from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from .models import User
from .serializers import *

# def login_form(request):
#     return render(request,"login_form.html")


class Users(APIView):
    # 신규 유저 등록
    def post(self,request) :
        serializer = UserSerializer(data=request.data)
        # is_valid 메서드로 유효성 검사 
        if serializer.is_valid() :
            user = serializer.save()
            # print("user.password : ", user.password)
            user.set_password(user.password) # set_password 가 pw를 해싱처리
            user.save()
            return Response(serializer.data)
        #저장실패시 오류사항 내역 출력
        return Response(serializer.errors)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    # 가져오는 pk(id)의 유저가 있는 지 조회
    def get_object(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
            
            # UserDetail에서는 조회(get)/수정(post)/삭제(delete) 모두 본인만 가능해야 하므로
            # get_object 자체에서 pk로 가져오는 유저와 현재 로그인 중인 유저가 동일한지 판단
            if not user == request.user :
                raise PermissionDenied
            
            return user
        except User.DoesNotExist :
            raise NotFound

    # 유저 한명 조회
    def get(self,request,pk):
        # get_object를 이용하여 유저 조회instance
        user = self.get_object(request,pk)
        serializer = UserOverviewSerializer(user)
        return Response(serializer.data)

    # 유저 수정    
    def put(self,request,pk):
        user = self.get_object(request,pk)
        serializer = UserOverviewSerializer(instance=user,data=request.data,partial=True) # 기존의 값, 요청(변경)값, 부분적 요청 명시
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # 유저 삭제
    def delete(self,request,pk):
        user = self.get_object(request,pk)
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)

# 전체 유저 조회 - admin 전용
class UsersList(APIView):
    # admin 유저만 접근 가능
    # permission_classes = [IsAdminUser]

    # 인가된 사용자 중
    permission_classes = [IsAuthenticated]

    # 유저 전체 조회
    def get(self,request):
        # staff 유저만 가능
        if request.user.is_staff :
            users = User.objects.all()
            serializer = UserAllSerializer(users,many=True)
            return Response(serializer.data)
        else :
            raise PermissionDenied
        

# 로그인
class Login(APIView) :
    def post(self, request) :
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        # Not None
        if user : 
            login(request, user)
            return Response({'login' : 'success'})
        else :
            return Response(status.HTTP_401_UNAUTHORIZED)
        
# 로그아웃
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        logout(request)
        return Response({"logout" : "success"})
    