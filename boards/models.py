from django.db import models

class Board(models.Model):
    # 글번호
    no = models.AutoField(primary_key=True) # auto_created=1000
    # 제목
    title = models.CharField(max_length=100)
    # 내용
    content = models.TextField(null=True,blank=True)
    # 작성자
    author = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL, # fk로 연결된 유저가 삭제될 경우 set null
        null=True,
        related_name='boards' # 역접근자 rename 가능
    ) 
    # 파일
    file = models.FileField(upload_to='uploads/', blank=True)
    # 이미지 링크
    image_url = models.URLField(default='')
    # 등록일
    create_at = models.DateTimeField(auto_now_add=True)
    # 수정일
    update_at = models.DateTimeField(auto_now=True)
