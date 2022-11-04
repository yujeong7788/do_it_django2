from django.test import TestCase,Client
from bs4 import BeautifulSoup
from .models import Post # 현재경로의 모델의 포스트를 가져와라
from django.contrib.auth.models import User

# Create your tests here.

class TestView(TestCase):
    def setUp(self): # 베이스 만드는곳임, 기본 환경 셋팅
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump',password='somepassword') # 계정생성
        self.user_obama = User.objects.create_user(username='obama',password='somepassword')
        
    def navbar_test(self,soup): # 함수 바깥에서 soup 받기
        navbar = soup.nav
        self.assertIn('Blog',navbar.text)
        self.assertIn('About Me',navbar.text)
        
        logo_btn = navbar.find('a',text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'],'/') # attrs : 속성 href라는 속성찾기, 속성여러개라 키값으로 찾기
        
        home_btn = navbar.find('a',text='Home')
        self.assertEqual(home_btn.attrs['href'],'/')
        
        blog_btn = navbar.find('a',text='Blog')
        self.assertEqual(blog_btn.attrs['href'],'/blog/')
        
        about_me_btn = navbar.find('a',text='About Me')
        self.assertEqual(about_me_btn.attrs['href'],'/about_me/')
        
    def test_post_list(self):
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
         
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code,200) # 정상 200 비정상 404
        
        # 1.3 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content,'html.parser') #받은 소스코드 넘어감, 구조화
        self.assertEqual(soup.title.text,'Blog')
       
        # # 1.4 네비게이션 바가 있다.
        # navbar = soup.nav # nav 태그 다 가져옴
        
        # # 1.5 Blog, Abou me 라는 문구가 네비게이션 바에 있다.
        # self.assertIn('Blog',navbar.text) # 나브 태그 안에 블로그가 있냐
        # self.assertIn('About Me',navbar.text)
        self.navbar_test(soup)
        
        # 2.1 메인 영역에 게시물이 하나도 없다면
        #self.assertEqual(Post.objects.count,0) #  포스트 개체의 오브젝트 갯수 0개
        
        # 2.2 '아직 게시물이 없습니다.'라는 문구가 보인다.
        main_area = soup.find('div',id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text) # 마침표 찍지말것
        
        # 3.1 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title='첫 번째 포스트 입니다.',
            content = 'Hello world. We are the World.',
            author = self.user_trump
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트 입니다.',
            content = '1등이 전부는 아니잖아요?',
            author = self.user_obama
        )
        self.assertEqual(Post.objects.count(),2)
        
        # 3.2 포스트 목록페이지를 새로고침했을때
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div',id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        
        # 3.4 '아직 게시물이 없습니다.'라는 문구를 더 이상 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다',main_area.text) # mainarea 텍스트값에 아직 게시물이 없습니다가 없으면 오케이
        
        self.assertIn(self.user_trump.username.upper(),main_area.text)
        self.assertIn(self.user_obama.username.upper(),main_area.text)

    def test_post_detail(self):
        
        # 1.1 포스트가 하나 있다.
        post_001 = Post.objects.create(
            title='첫 번째 포스트 입니다.',
            content = 'Hello world. We are the World.',
            author = self.user_trump
        )
                
        # 1.2 그 포스트의 url은 '/blog/1'
        self.assertEqual(post_001.get_absolute_url(),'/blog/1/') #함수호출 괄호 필수
        
        # 2 첫번째 포스트의 상세 페이지 테스트
        # 2.1 첫번째 포스트의 url로 접근하면 정상적으로 작동한다.
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser') # 구조화?  
        
        # # 2.2 포스트 목록 페이지와 똑같은 네비게이션 바가 있다.
        # navbar = soup.nav
        # self.assertIn('Blog',navbar.text)
        # self.assertIn('About Me',navbar.text)
        self.navbar_test(soup)
        
        # 2.3 첫번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(post_001.title,soup.title.text)
        
        # 2.4 첫번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div',id='main-area')
        post_area = main_area.find('div',id='post-area')
        self.assertIn(post_001.title,post_area.text)
        
        # 2.5 첫번째 포스트의 작성자가 포스트 영역에있다(아직 구현x)
        self.assertIn(self.user_trump.username.upper(),post_area.text)
        
        # 2.6 첫번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(post_001.content,post_area.text)
        
    # def test_post_list(self):
    #     self.assertEqual(2,2) # 같으면 ok, 다르면 오류 발생
        
    
    