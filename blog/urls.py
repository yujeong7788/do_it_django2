from django.urls import path
from . import views  # url이랑(url.py) 실행할 함수(views.py)가 따로 떨어져있음 -> views import 해야함

# urlpatterns = [
#     path('',views.index), # "blog/"라는 요청이 들어오면 views 안에 있는 index 함수를 호출하라
#     path('<int:pk>/',views.single_post_page), # "blog/<int:pk>/" 라는 요청이 들어오면 views 안에 있는 single_post_page 함수를 호출

# ]
# flask에서의 app.route랑 비슷한 역할을 하는 urlpatterns

# urlpatterns = [
#     path('',views.PostList.as_view()),  # blog/views.py의 class를 호출
#     path('<int:pk>/',views.single_post_page)
# ]

urlpatterns = [
    path('',views.PostList.as_view()),  # blog/views.py의 class를 호출
    path('<int:pk>/',views.PostDetail.as_view())
]