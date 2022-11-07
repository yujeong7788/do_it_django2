from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) # unique = True 똑같은 글자 허용 , 유니코드 허용
    #slug 안되는 기호 알아서 자동으로 바꿔줌
    
    def __str__(self):
        return self.name #이름값 나타나게
    
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'
    
    

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) # unique = True 똑같은 글자 허용 , 유니코드 허용
    #slug 안되는 기호 알아서 자동으로 바꿔줌
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
    
    
    class Meta:
        verbose_name_plural ="Categories" # s붙여주는역할

class Post(models.Model): # Post라는 이름의 클래스는 modes의 Model을 상속받음. 
    title = models.CharField(max_length=30)# CharField() : 한 줄짜리 문자 필드, 최대 30
    # 모델이 어떻게 만들어져야 하는지를 부모로 부터 상속받음
    # pk는 알아서 만들어줌(우리가 지정 안해도 됨)
    # 데이터타입, 길이값, null/not-null
    hook_text = models.CharField(max_length=100,blank=True) # 짧은글, blank = True : null값 허용 , 비워도됨
    content = models.TextField() # textarray?텍스트 어레이랑 연결됨(여러 줄짜리 문자 필드)
    
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/',blank=True)  
    # 이미지인지(ImageField), 일반 파일(FileField)인지에 따라서 달리 씀
    # /%Y/%m/%d/ 연월일
    # blank=True : 이미지 없어도 가능
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/',blank=True) # 모든파일 가능 엑셀 이미지 등등
    
    create_at = models.DateTimeField(auto_now_add=True)
    # author : 추후 작성 예정
    # 모델의 필드 관련된 내용이 변경되면 makemigrations 변경사항 집계함
    # DateTimeField(auto_now_add=True) : 자동으로 날짜시간 생성됨
    update_at = models.DateTimeField(auto_now=True)
    # 수정되었을 때 현재시간으로 넣어줌
    # 모델의 필드 하나 수정, 하나 생성됨 -> migration 필요

    author = models.ForeignKey(User,null=True,on_delete=models.SET_NULL) # 테이블명만 적으면 유저에 있는 아이디 참조함,CASCADE : User 삭제하면 유저가 작성한 글도 같이 삭제됨, null은 삭제해ㅐ도 안없어짐
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL,blank=True) # 제거되면 널값으로 채우겠다 이게맞음..
    tags = models.ManyToManyField(Tag,blank=True) # 태그 모델에 있는 널값 트루 널 허용, 블랭크도 트루 비워두는거 가능

    
    
    def __str__(self): # class 인자는 무조건 자기자신(self)?
        return f'[{self.id}] {self.title} :: {self.author}' # [글번호]
    # 함수 추가 -> migration 안 해도 됨
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'  # blog/pk값 들어가게
    
    def get_file_name(self):
        return os.path.basename(self.file_upload.name) # 디렉토리 빼고 파일명과 확장자를 빼줌, 파일업로드네임에서 찾을거다

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #보통은ㅇ 마지막ㅇ에 있는거 가져오는게 좋음
    
