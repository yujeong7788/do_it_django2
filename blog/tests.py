from django.test import TestCase,Client
from bs4 import BeautifulSoup
from .models import Post, Category # 현재경로의 모델의 포스트를 가져와라
from django.contrib.auth.models import User

# Create your tests here.

class TestView(TestCase):
    def setUp(self): # 베이스 만드는곳임, 기본 환경 셋팅
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump',password='somepassword') # 계정생성
        self.user_obama = User.objects.create_user(username='obama',password='somepassword')
        self.category_programing = Category.objects.create(name='programming',slug='programming')
        self.category_music = Category.objects.create(name='music',slug='music')
        self.post_001 = Post.objects.create(
                title='첫 번째 포스트 입니다.',
                content = 'Hello world. We are the World.',
                category = self.category_programing,
                author = self.user_trump
        )
        self.post_002 = Post.objects.create(
                title='두 번째 포스트 입니다.',
                content = '1등이 전부는 아니잖아요?',
                category = self.category_music,
                author = self.user_obama
        )
        self.post_003 = Post.objects.create(
                title='세 번째 포스트 입니다.',
                content = '2등이 전부는 아니잖아요?',
                author = self.user_obama
        )
        
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
        
    def category_card_test(self,soup):
        category_card = soup.find('div',id='categories-card')
        self.assertIn('Categories',category_card.text)
        self.assertIn(f'{self.category_programing.name} ({self.category_programing.post_set.count()})',category_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})',category_card.text)
        self.assertIn(f'미분류 (1)',category_card.text)
        
    def test_post_list(self):
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(),3)
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code,200) # 정상 200 비정상 404
        soup = BeautifulSoup(response.content,'html.parser') #받은 소스코드 넘어감, 구조화
        self.navbar_test(soup)
        self.category_card_test(soup)
        
        main_area = soup.find('div',id='main-area')
        self.assertNotIn('아직 게시물이 없습니다',main_area.text) # mainarea 텍스트값에 아직 게시물이 없습니다가 없으면 오케이
        
        
        post_001_card = main_area.find('div',id='post-1')
        self.assertIn(self.post_001.title,post_001_card.text)
        self.assertIn(self.post_001.category.name,post_001_card.text)
        
        post_002_card = main_area.find('div',id='post-2')
        self.assertIn(self.post_002.title,post_002_card.text)
        self.assertIn(self.post_002.category.name,post_002_card.text)
        
        post_003_card = main_area.find('div',id='post-3')
        self.assertIn(self.post_003.title,post_003_card.text)
        self.assertIn('미분류',post_003_card.text)
        
        self.assertIn(self.user_trump.username.upper(),main_area.text)
        self.assertIn(self.user_obama.username.upper(),main_area.text)
        
        # 포스트가 없는 경우
        Post.objects.all().delete() # 모든 게시물 삭제
        self.assertEqual(Post.objects.count(),0) #  포스트 개체의 오브젝트 갯수 0개
        
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        main_area = soup.find('div',id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text) # 마침표 찍지말것
        
        main_area = soup.find('div',id='main-area')
        self.assertIn('아직 게시물이 없습니다',main_area.text)

    def test_post_detail(self):
        
        self.assertEqual(self.post_001.get_absolute_url(),'/blog/1/') #함수호출 괄호 필수
        
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser') # 구조화한다.
        self.navbar_test(soup)
        self.category_card_test(soup)
        
        self.assertIn(self.post_001.title,soup.text)
        
        main_area = soup.find('div',id='main-area')
        post_area = main_area.find('div',id='post-area')
        self.assertIn(self.post_001.title,post_area.text)
        self.assertIn(self.category_programing.name,post_area.text)
        
        self.assertIn(self.user_trump.username.upper(),post_area.text)
        
        self.assertIn(self.post_001.content,post_area.text)
        
    # def test_post_list(self):
    #     self.assertEqual(2,2) # 같으면 ok, 다르면 오류 발생
        
        
    def test_category_page(self):
        response = self.client.get(self.category_programing.get_absolute_url())
        self.assertEqual(response.status_code,200)

        soup = BeautifulSoup(response.content,'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_programing.name,soup.h1.text)

        main_area =soup.find('div',id='main-area')
        self.assertIn(self.category_programing.name,main_area.text)
        self.assertIn(self.post_001.title,main_area.text)
        self.assertNotIn(self.post_002.title,main_area.text)
        self.assertNotIn(self.post_003.title,main_area.text)
    
    