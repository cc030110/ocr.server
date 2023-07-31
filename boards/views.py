from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from .models import Board
from .serializers import BoardSerializer

from pyuploadcare import Uploadcare, File
from django.conf import settings


# views -> 사용자에게 보여지는 화면

# def board_form(request):
#     return render(request,"board_form.html",{
#         "data" : Board.objects.all()
#     }) # render(요청값, 이동페이지, {전달 데이터 <- dict()})

# rest_framework
# @api_view(['GET','POST'])
# def get_board_all(request):
#     boards = Board.objects.all()
#     # boards를 JSON 으로 형변환 필요 (rest_framework -> Serializer)
#     serializer = BoardSerializer(boards, many=True)
#     return Response(serializer.data)

class Boards(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request) :
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    def post(self, request) :
        serializer = BoardSerializer(data=request.data)

        if serializer.is_valid() :
            board = serializer.save() # create() 메소드를 호출하게 됨 

            if board.file and board.file.size < settings.FILE_SIZE_LIMIT :
                uploadcare = Uploadcare(public_key=settings.UC_PUBLIC_KEY, secret_key=settings.UC_SECRET_KEY)
                with open(board.file.path, 'rb') as file_object:
                    ucare_file = uploadcare.upload(file_object)
                    image_url = f"https://ucarecdn.com/{ucare_file.uuid}/"
                    board.image_url = image_url

            board.author = request.user
            board.save()
            return redirect(f'/board/{board.pk}')

        return Response(serializer.errors)
    

class BoardDetail(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk) :
        try :
            board = Board.objects.get(pk=pk)
            return board
        except Board.DoesNotExist :
            raise NotFound

    def get(self, request, pk) :
        # pk를 가져와서 -> 보드 한개 가져오기 
        board = self.get_object(pk)
        # 보드 인스턴스를 -> JSON 형변환
        serializer = BoardSerializer(board)
        # Response 객체로 반환  
        return Response(serializer.data)
        
    def put(self, request, pk) :
        board = self.get_object(pk)

        if not board.author == request.user : 
            raise PermissionDenied

        serializer = BoardSerializer(instance=board, data=request.data, partial=True)

        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    def delete(self, request, pk) :
        board = self.get_object(pk)

        if not board.author == request.user : 
            raise PermissionDenied

        board.delete()
        return Response({})
    
