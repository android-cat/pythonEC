"""
Authentication Views - 認証関連
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from accounts.forms import SignUpForm
import logging

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    """カスタムログインビュー"""
    template_name = 'accounts/login.html'
    
    def get_form(self, form_class=None):
        logger.debug("get_form が呼ばれました")
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ユーザー名'
        })
        form.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワード'
        })
        return form
    
    def form_valid(self, form):
        logger.info(f"ログイン成功: ユーザー={form.get_user()}")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.warning(f"ログイン失敗: エラー={form.errors}")
        logger.warning(f"入力されたユーザー名: {form.data.get('username')}")
        return super().form_invalid(form)


def signup(request):
    """ユーザー登録ビュー"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'アカウントを作成しました。')
            return redirect('shop:product_list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    """ログアウトビュー（GET/POSTどちらでも対応）"""
    logger.info(f"ログアウト: ユーザー={request.user}")
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('accounts:login')
