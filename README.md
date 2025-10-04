# Django ECサイト

DjangoのMTV（Model-Template-View）パターンで構築されたEコマースサイトです。

## 機能

- 商品一覧・詳細表示
- カテゴリ別商品表示
- ショッピングカート機能（ログイン不要）
- 注文管理（注文履歴、詳細表示）
- ユーザー認証（登録、ログイン、プロフィール）
- 管理者画面（商品・注文・ユーザー管理）

## 技術スタック

- **Backend**: Django 4.2+
- **Database**: SQLite3（開発環境）
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Image Processing**: Pillow

## クイックスタート

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. データベースのマイグレーション
```bash
# マイグレーション作成
python manage.py makemigrations

# マイグレーション適用
python manage.py migrate
```

### 3. 管理者ユーザーの作成
```bash
python manage.py createsuperuser
```

### 4. 開発サーバーの起動
```bash
python manage.py runserver
```

### 5. 初期データ登録

ブラウザで http://localhost:8000/admin/ にアクセスし、以下を登録:
1. カテゴリを追加（例: 電子機器、書籍、衣料品）
2. 商品を追加（カテゴリ、価格、在庫数を設定）

### 6. サイトへアクセス

http://localhost:8000/ でECサイトのトップページが表示されます。

## プロジェクト構造（MVCアーキテクチャ）

```
pythonEC/
├── config/                    # プロジェクト設定
│   ├── settings.py           # Django設定
│   ├── urls.py               # URLルーティング
│   ├── middleware.py         # カスタムミドルウェア
│   └── wsgi.py               # WSGIエントリーポイント
├── shop/                     # ECサイトメインアプリ
│   ├── models/               # Model層（データモデル）
│   │   ├── category.py      # カテゴリモデル
│   │   ├── product.py       # 商品モデル
│   │   ├── cart.py          # カートモデル
│   │   └── order.py         # 注文モデル
│   ├── views/                # View層（コントローラー）
│   │   ├── product_views.py # 商品ビュー
│   │   ├── cart_views.py    # カートビュー
│   │   └── order_views.py   # 注文ビュー
│   ├── services/             # Service層（ビジネスロジック）
│   │   ├── cart_service.py  # カート管理ロジック
│   │   └── order_service.py # 注文管理ロジック
│   ├── forms/                # Form層（フォーム定義）
│   │   └── order_form.py    # 注文フォーム
│   ├── admin/                # Admin層（管理画面）
│   │   ├── product_admin.py # 商品管理
│   │   ├── cart_admin.py    # カート管理
│   │   └── order_admin.py   # 注文管理
│   ├── utils/                # Utility層
│   │   └── context_processors.py
│   └── urls.py               # URLパターン
├── accounts/                 # ユーザー認証アプリ
│   ├── views/
│   │   ├── auth_views.py    # 認証ビュー
│   │   └── profile_views.py # プロフィールビュー
│   ├── forms/
│   │   └── signup_form.py   # 登録フォーム
│   └── urls.py
├── templates/                # Template層（HTMLテンプレート）
│   ├── base.html
│   ├── shop/
│   └── accounts/
├── static/                   # 静的ファイル
│   └── css/
├── media/                    # アップロードファイル
├── README.md                 # プロジェクト概要
├── design/                    # 設計書フォルダ
│   ├── ARCHITECTURE.md       # アーキテクチャ設計書
│   ├── DESIGN.md             # システム設計書
│   ├── API_SPEC.md           # API仕様書
│   └── OPERATION.md          # 運用マニュアル
```

**MVCアーキテクチャの詳細**: [ARCHITECTURE.md](ARCHITECTURE.md) を参照

## ドキュメント

- **[DESIGN.md](DESIGN.md)**: システム設計書（データベース設計、機能仕様）
- **[API_SPEC.md](API_SPEC.md)**: API仕様書（将来的なREST API化）
- **[OPERATION.md](OPERATION.md)**: 運用マニュアル（日常運用、トラブルシューティング）

## 主な機能

### 1. 商品管理
- 商品の登録・編集・削除
- カテゴリ別表示
- 在庫管理
- 商品画像アップロード

### 2. カート機能
- ログイン不要でカート利用可能
- 商品の追加・削除・数量変更
- リアルタイム合計金額計算

### 3. 注文機能
- 配送先情報入力
- 注文確定・履歴表示
- 注文ステータス管理（注文受付、処理中、発送済み、配達完了、キャンセル）

### 4. ユーザー認証
- ユーザー登録・ログイン・ログアウト
- プロフィール表示
- 注文履歴確認

### 5. 管理機能
- Django管理画面
- 商品・注文・ユーザー管理
- 在庫・価格の一括編集

## トラブルシューティング

### マイグレーションエラー
```bash
python manage.py makemigrations shop accounts
python manage.py migrate
```

### 管理画面でログインできない
- ユーザー名（メールアドレスではない）でログイン
- パスワードリセット: `python manage.py changepassword <username>`

### 画像が表示されない
- `media/`フォルダが存在することを確認
- `settings.py`の`MEDIA_URL`と`MEDIA_ROOT`を確認
- 開発サーバーの場合、`DEBUG=True`であることを確認

詳細は [OPERATION.md](OPERATION.md) を参照してください。

## セキュリティ

本番環境にデプロイする前に:
- [ ] `DEBUG = False`に設定
- [ ] `SECRET_KEY`を環境変数から読み込み
- [ ] `ALLOWED_HOSTS`を設定
- [ ] データベースを本番用に変更
- [ ] HTTPSを有効化

```bash
# セキュリティチェック
python manage.py check --deploy
```

## ライセンス

MIT License

## 作成日

2025年10月4日
