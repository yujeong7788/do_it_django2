from django.urls import path
from . import views  # url이랑(url.py) 실행할 함수(views.py)가 따로 떨어져있음 -> views import 해야함

urlpatterns = [
    path('',views.PostList.as_view()),  # blog/views.py의 class를 호출
    path('<int:pk>/',views.PostDetail.as_view()),
    path('category/<str:slug>/',views.category_page),
    path('tag/<str:slug>/',views.tag_page),
    path('create_post/',views.PostCreate.as_view()),
    path('update_post/<int:pk>/',views.PostUpdate.as_view())
]