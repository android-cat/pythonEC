"""
Test Auth Views
認証ビューのテスト
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class LoginViewTest(TestCase):
    """ログインビューのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_login_view_status_code(self):
        """ログインページが正常に表示されることを確認"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_uses_correct_template(self):
        """正しいテンプレートが使用されていることを確認"""
        response = self.client.get(reverse('accounts:login'))
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_login_with_valid_credentials(self):
        """正しい認証情報でログインできることを確認"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # ログイン成功後、トップページにリダイレクト
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.url)
        
        # ユーザーがログイン状態になっていることを確認
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_with_invalid_credentials(self):
        """無効な認証情報でログインできないことを確認"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        # ログイン失敗時はログインページを再表示
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class LogoutViewTest(TestCase):
    """ログアウトビューのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_logout_view_get(self):
        """GETリクエストでログアウトできることを確認"""
        # ログイン
        self.client.login(username='testuser', password='testpass123')
        
        # ログアウト
        response = self.client.get(reverse('accounts:logout'))
        
        # ログインページにリダイレクト
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_logout_view_post(self):
        """POSTリクエストでログアウトできることを確認"""
        # ログイン
        self.client.login(username='testuser', password='testpass123')
        
        # ログアウト
        response = self.client.post(reverse('accounts:logout'))
        
        # ログインページにリダイレクト
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)


class SignupViewTest(TestCase):
    """サインアップビューのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
    
    def test_signup_view_status_code(self):
        """サインアップページが正常に表示されることを確認"""
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_signup_view_uses_correct_template(self):
        """正しいテンプレートが使用されていることを確認"""
        response = self.client.get(reverse('accounts:signup'))
        self.assertTemplateUsed(response, 'accounts/signup.html')
    
    def test_signup_with_valid_data(self):
        """正しいデータでサインアップできることを確認"""
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!'
        })
        
        # サインアップ成功後、トップページにリダイレクト
        self.assertEqual(response.status_code, 302)
        
        # ユーザーが作成されていることを確認
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # 自動的にログイン状態になっていることを確認
        user = User.objects.get(username='newuser')
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
    
    def test_signup_with_duplicate_username(self):
        """既存のユーザー名でサインアップできないことを確認"""
        # 既存ユーザーを作成
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='ExistingPass123!'
        )
        
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!'
        })
        
        # サインアップ失敗時はサインアップページを再表示
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 
                           'A user with that username already exists.')


class ProfileViewTest(TestCase):
    """プロフィールビューのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_profile_requires_login(self):
        """プロフィールページにはログインが必要"""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_profile_view_with_authenticated_user(self):
        """ログイン済みユーザーはプロフィールページを表示できる"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.context['user'], self.user)
