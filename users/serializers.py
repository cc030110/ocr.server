from rest_framework.serializers import ModelSerializer
from .models import User

# serializer -> JSON 형변환을 해줌

# 유저 등록
class UserSerializer(ModelSerializer):
    class Meta:
      model = User
      # fields = "__all__" # 필드 전체
      fields = [
         "username",
         "password",
         "name",
         "email",
         "is_active",
      ]

# 유저 조회, 수정
class UserOverviewSerializer(ModelSerializer):
   class Meta :
      model=User
      fields = [
         "username",
         "name",
         "email",
      ]

# 유저의 모든 정보 조회 - admin용
class UserAllSerializer(ModelSerializer):
   class Meta :
      model = User
      fields ="__all__"