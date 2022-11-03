from django.contrib import admin
from .models import Post  # . : 현재 경로 기준으로 # models.py 안에 Post라는 클래스 임포트
# Register your models here.
admin.site.register(Post)
# 모델의 필드가 변경될 때(함수가 변경될 때는 안해도 됨) migrate나 migration함