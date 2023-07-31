from rest_framework.serializers import ModelSerializer
from .models import Board
from users.serializers import UserOverviewSerializer

class BoardSerializer(ModelSerializer):
    author = UserOverviewSerializer(read_only=True)
    class Meta :
      model = Board
      fields = "__all__" # 필드 전체
      # depth = 1 # 모든정보 <- 보안 위험
      # fields = [ # 내가 원하는 것만
      #     "title",
      #     "content",
      #     "author",
      # ]
      # exclude = [ # 제외
      #    "update_at",
      # ]
