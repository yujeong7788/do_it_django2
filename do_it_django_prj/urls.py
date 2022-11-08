
from django.contrib import admin
from django.urls import path, include # urls 파일 하나가 아니라 다른 데에 있는 것을 불러와 사용

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("blog/",include('blog.urls')), # blog/라는 요청이 들어오면 blog 아래에 있는 urls를 불러와 사용
    path("admin/", admin.site.urls),
    path("", include('single_pages.urls')),
    path('markdownx/',include('markdownx.urls'))
]
# flask에서의 app.route랑 비슷한 역할을 하는 urlpatterns
# admin 하나만 활성화됨(관리자 계정 가는 url)
# admin/ 아래 나오는 하위 경로는 admin.site.urls에서 처리

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)