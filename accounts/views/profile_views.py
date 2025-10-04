"""
Profile Views - プロフィール関連
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """プロフィール表示ビュー"""
    return render(request, 'accounts/profile.html')
