"""do_it_django_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # urls 파일 하나가 아니라 다른 데에 있는 것을 불러와 사용

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("blog/",include('blog.urls')), # blog/라는 요청이 들어오면 blog 아래에 있는 urls를 불러와 사용
    path("admin/", admin.site.urls),
    path("", include('single_pages.urls')),
]
# flask에서의 app.route랑 비슷한 역할을 하는 urlpatterns
# admin 하나만 활성화됨(관리자 계정 가는 url)
# admin/ 아래 나오는 하위 경로는 admin.site.urls에서 처리

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)