from django.urls import path
from . import views  # url이랑(url.py) 실행할 함수(views.py)가 따로 떨어져있음 -> views import 해야함

urlpatterns = [
    path('about_me/',views.about_me),  
    path('',views.landing),
]