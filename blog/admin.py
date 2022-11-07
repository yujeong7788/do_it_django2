from django.contrib import admin
from .models import Post,Category,Tag  # . : 현재 경로 기준으로 # models.py 안에 Post라는 클래스 임포트
# Register your models here.
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    # 자동으로 입력 ~~~
    
admin.site.register(Category,CategoryAdmin)
# 모델의 필드가 변경될 때(함수가 변경될 때는 안해도 됨) migrate나 migration함

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
admin.site.register(Tag,TagAdmin)
    