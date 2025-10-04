"""
Test Signup Form
サインアップフォームのテスト
"""
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import SignUpForm


class SignUpFormTest(TestCase):
    """サインアップフォームのテストケース"""
    
    def test_signup_form_valid_data(self):
        """正しいデータでフォームが有効になることを確認"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_signup_form_missing_username(self):
        """ユーザー名が欠落しているとエラー"""
        form_data = {
            'username': '',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_signup_form_missing_email(self):
        """メールアドレスが欠落しているとエラー"""
        form_data = {
            'username': 'testuser',
            'email': '',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_signup_form_invalid_email(self):
        """無効なメールアドレスでエラー"""
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_signup_form_password_mismatch(self):
        """パスワードが一致しないとエラー"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'DifferentPass123!'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_signup_form_duplicate_username(self):
        """既存のユーザー名でエラー"""
        # 既存ユーザーを作成
        User.objects.create_user(
            username='testuser',
            email='existing@example.com',
            password='ExistingPass123!'
        )
        
        form_data = {
            'username': 'testuser',
            'email': 'new@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_signup_form_saves_user(self):
        """フォームが正しくユーザーを保存することを確認"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('NewPass123!'))
    
    def test_signup_form_widget_attributes(self):
        """フォームウィジェットに正しい属性が設定されていることを確認"""
        form = SignUpForm()
        
        # クラス属性が設定されていることを確認
        self.assertIn('form-control', form.fields['username'].widget.attrs['class'])
        self.assertIn('form-control', form.fields['email'].widget.attrs['class'])
        self.assertIn('form-control', form.fields['password1'].widget.attrs['class'])
        self.assertIn('form-control', form.fields['password2'].widget.attrs['class'])
