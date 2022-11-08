from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView
# 목록 중 글 하나를 보는 것은 DetailView, 수정은 UpdateView ... 클래스가 이미 정해져있음
from .models import Post,Category,Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
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
        post_list = Post.objects.filter(category=None).order_by('-pk')
    else:    
        category = Category.objects.get(slug=slug) # url에서 받음
        post_list = Post.objects.filter(category=category).order_by('-pk')
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
    post_list = tag.post_set.all().order_by('-pk')
    
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
    
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=Post
    fields=['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user # 로그인한 정보 넣어주는곳
            response = super(PostCreate,self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag,is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t,allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            else:
                return response
                            
            return response
        else:
            return redirect('/blog/')
    
    
class PostUpdate(LoginRequiredMixin,UpdateView):
    model=Post
    fields=['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category'] #수정하고자하는 항목
    
    template_name = 'blog/post_update_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(PostUpdate,self).get_context_data()
        if self.object.tags.exists():# object 안에 가져온값 담겨져있음
            tags_str_list = list()
            for t in self.object.tags.all(): # 태그 전부 다 가져와서  t에 받아
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author: # 로그인 됐는지 확인 and 요청한사람과 작성자 일치한지 화깅ㄴ
            return super(PostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def form_valid(self, form):
        response = super(PostUpdate,self).form_valid(form)
        self.object.tags.clear()
        
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
                tags_str = tags_str.strip() # 공백제거
                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag,is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t,allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
        return response