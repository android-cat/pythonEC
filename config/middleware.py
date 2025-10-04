import logging

logger = logging.getLogger(__name__)


class RequestResponseLoggingMiddleware:
    """リクエストとレスポンスをログに記録するミドルウェア"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # リクエストのログ
        logger.info(f"=== リクエスト ===")
        logger.info(f"メソッド: {request.method}")
        logger.info(f"パス: {request.path}")
        logger.info(f"ユーザー: {request.user}")
        logger.info(f"認証済み: {request.user.is_authenticated}")
        
        if request.method == 'POST':
            logger.info(f"POSTデータ: {dict(request.POST)}")
            # パスワードは表示しない
            post_data = dict(request.POST)
            if 'password' in post_data:
                post_data['password'] = ['***隠されています***']
            if 'password1' in post_data:
                post_data['password1'] = ['***隠されています***']
            if 'password2' in post_data:
                post_data['password2'] = ['***隠されています***']
            logger.info(f"POSTデータ(安全): {post_data}")
        
        logger.info(f"GETパラメータ: {dict(request.GET)}")
        logger.info(f"セッション: {dict(request.session) if hasattr(request, 'session') else 'なし'}")

        # レスポンスを取得
        response = self.get_response(request)

        # レスポンスのログ
        logger.info(f"=== レスポンス ===")
        logger.info(f"ステータスコード: {response.status_code}")
        logger.info(f"リダイレクト: {response.get('Location', 'なし')}")
        logger.info(f"ユーザー(レスポンス後): {request.user}")
        logger.info(f"認証済み(レスポンス後): {request.user.is_authenticated}")
        logger.info(f"=" * 50)

        return response
