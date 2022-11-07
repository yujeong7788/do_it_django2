from django.shortcuts import render
from django.views.generic import ListView, DetailView
# 목록 중 글 하나를 보는 것은 DetailView, 수정은 UpdateView ... 클래스가 이미 정해져있음
from .models import Post,Category,Tag
# 현재 경로에 있는 models 안의 Post 임포트
# Create your views here.

# def index(request): 
#     # index() 안에 request 개체를 꼭 적어야 함 request 개체 안에는 클라이언트로부터 전달받은 데이터, 방식 등이 들어 있음
#     # render -> flask의 rendertemplate과 비슷한 역할, request 적어야 함
#     posts = Post.objects.all().order_by('-pk') 
#     # object(이미 만들어져있음)에 있는 데이터를 다 들고 와 posts에 저장
#     # order_by('-pk') : -를 붙이면 내림차순(pk=id를 기준으로 내림차순됨) -> 최신글 먼저 정렬
#     return render(
#         request,
#     'blog/index.html',
#     {
#         'posts':posts,
#     }
#     ) # 딕셔너리롤 만들어서 넘겨줘야 함, posts를 랜더링할 때 같이 보내줌?
#     # blog앱 안에 template을 만들어 넣어줌, single_page 앱 안에도 template -> 이름이 중복되는 상황 발생 가능
#     # 각 앱의 탬플릿이 하나의 템플릿으로 모아져서 처리됨 -> 이름이 중복되면 문제 생길 수 있음
#     # blog/ 호출 시 : 프로젝트의 urls.py 호출됨 -> blog 쪽의 urls.py로 감 -> views.index로 가라 -> views.py의 index함수로 감

class PostList(ListView): # ListView에서 상속받음
    model = Post  # Post 모델 사용
    ordering='-pk'
    # template_name = "blog/index.html"
    
    def get_context_data(self,**kwargs): # 파라미터 * 변수명 : 리스트로 받음 , ** : 키 value로 받음 딕셔너리로받는다.
        context = super(PostList,self).get_context_data() # super 부모 생성자에 자기 개체이름 넣고 부모의 get_context_data호출, 전체 데이터 호출
        # == context['post_list']= Post.objects.all()
        context['categories'] = Category.objects.all() #키 이름으로 바로 호출
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
        

    
    
# def single_post_page(request,pk): # urls.py의 <int:pk>를 함수의 인자로 넣어야 하니(flask때 참고) pk도 인자로 넣음
#     post = Post.objects.get(pk=pk) # 하나만 가져올 때는 get, 다 가져올 때는 all
#     # pk=pk이면 하나 가져옴
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post':post,
#         }
#     )

class PostDetail(DetailView): # DetailView에서 상속받음
    model = Post  # Post 모델 사용
    def get_context_data(self,**kwargs): # 파라미터 * 변수명 : 리스트로 받음 , ** : 키 value로 받음 딕셔너리로받는다.
        context = super(PostDetail,self).get_context_data() # super 부모 생성자에 자기 개체이름 넣고 부모의 get_context_data호출, 전체 데이터 호출
        # == context['post_list']= Post.objects.all()
        context['categories'] = Category.objects.all() #키 이름으로 바로 호출
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    
def category_page(request,slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:    
        category = Category.objects.get(slug=slug) # url에서 받음
        post_list = Post.objects.filter(category=category)
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list':post_list,
            'categories':Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category':category
        }
    )
    
def tag_page(request,slug):
    tag = Tag.objects.get(slug=slug) # 하나가져올때 겟
    post_list = tag.post_set.all()
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list':post_list,
            'tag' : tag,
            'categories' : Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
        }
    )