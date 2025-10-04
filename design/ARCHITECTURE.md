# プロジェクト構造 - MVCアーキテクチャ

## 📁 フォルダ構成

```
pythonEC/
├── 📁 config/                    # プロジェクト設定
│   ├── __init__.py
│   ├── settings.py              # Django設定
│   ├── urls.py                  # ルートURLルーティング
│   ├── middleware.py            # カスタムミドルウェア
│   ├── wsgi.py                  # WSGIエントリーポイント
│   └── asgi.py                  # ASGIエントリーポイント
│
├── 📁 shop/                      # ECサイトメインアプリ
│   ├── 📁 models/               # 🗄️ MODEL層（データモデル）
│   │   ├── __init__.py
│   │   ├── category.py          # カテゴリモデル
│   │   ├── product.py           # 商品モデル
│   │   ├── cart.py              # カート・カート商品モデル
│   │   └── order.py             # 注文・注文商品モデル
│   │
│   ├── 📁 views/                # 🎮 VIEW層（コントローラー）
│   │   ├── __init__.py
│   │   ├── product_views.py    # 商品表示ビュー
│   │   ├── cart_views.py       # カート操作ビュー
│   │   └── order_views.py      # 注文処理ビュー
│   │
│   ├── 📁 services/             # 💼 SERVICE層（ビジネスロジック）
│   │   ├── __init__.py
│   │   ├── cart_service.py     # カート管理ロジック
│   │   └── order_service.py    # 注文管理ロジック
│   │
│   ├── 📁 forms/                # 📝 FORM層（フォーム定義）
│   │   ├── __init__.py
│   │   └── order_form.py       # 注文フォーム
│   │
│   ├── 📁 admin/                # ⚙️ ADMIN層（管理画面）
│   │   ├── __init__.py
│   │   ├── product_admin.py    # 商品管理画面
│   │   ├── cart_admin.py       # カート管理画面
│   │   └── order_admin.py      # 注文管理画面
│   │
│   ├── 📁 utils/                # 🔧 UTILITY層（ユーティリティ）
│   │   ├── __init__.py
│   │   └── context_processors.py  # コンテキストプロセッサ
│   │
│   ├── 📁 migrations/           # データベースマイグレーション
│   ├── __init__.py
│   ├── apps.py                  # アプリ設定
│   └── urls.py                  # URLパターン
│
├── 📁 accounts/                  # ユーザー認証アプリ
│   ├── 📁 models/               # モデル層
│   │   └── __init__.py
│   │
│   ├── 📁 views/                # ビュー層
│   │   ├── __init__.py
│   │   ├── auth_views.py       # 認証ビュー
│   │   └── profile_views.py    # プロフィールビュー
│   │
│   ├── 📁 forms/                # フォーム層
│   │   ├── __init__.py
│   │   └── signup_form.py      # 登録フォーム
│   │
│   ├── __init__.py
│   ├── admin.py                 # 管理画面設定
│   ├── apps.py                  # アプリ設定
│   └── urls.py                  # URLパターン
│
├── 📁 templates/                 # 🎨 TEMPLATE層（ビュー）
│   ├── base.html                # ベーステンプレート
│   ├── 📁 shop/                 # ショップテンプレート
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_complete.html
│   │   ├── order_history.html
│   │   └── order_detail.html
│   │
│   └── 📁 accounts/             # アカウントテンプレート
│       ├── login.html
│       ├── signup.html
│       └── profile.html
│
├── 📁 static/                    # 静的ファイル
│   └── 📁 css/
│       └── style.css
│
├── 📁 media/                     # アップロードファイル
│   └── 📁 products/             # 商品画像
│
├── 📄 manage.py                  # Django管理コマンド
├── 📄 requirements.txt           # Python依存関係
├── 📄 db.sqlite3                 # データベース（開発環境）
├── 📄 .gitignore                 # Git除外設定
├── 📄 README.md                  # プロジェクト概要
├── 📄 DESIGN.md                  # 設計書
├── 📄 API_SPEC.md                # API仕様書
└── 📄 OPERATION.md               # 運用マニュアル
```

## 🏗️ MVCアーキテクチャの層構造

### 1. Model層（データ層）
**場所**: `shop/models/`, `accounts/models/`

**責務**:
- データベーステーブルの定義
- データの検証ルール
- データ間のリレーション定義
- プロパティメソッド（計算値）

**ファイル構成**:
```python
models/
├── __init__.py          # モデルのエクスポート
├── category.py          # カテゴリモデル
├── product.py           # 商品モデル
├── cart.py              # カート関連モデル
└── order.py             # 注文関連モデル
```

### 2. View層（コントローラー層）
**場所**: `shop/views/`, `accounts/views/`

**責務**:
- HTTPリクエストの処理
- ビジネスロジック層（Service）の呼び出し
- テンプレートへのデータ渡し
- HTTPレスポンスの返却

**ファイル構成**:
```python
views/
├── __init__.py          # ビューのエクスポート
├── product_views.py     # 商品表示ビュー
├── cart_views.py        # カート操作ビュー
└── order_views.py       # 注文処理ビュー
```

### 3. Template層（プレゼンテーション層）
**場所**: `templates/`

**責務**:
- HTMLの生成
- データの表示
- ユーザーインターフェース

### 4. Service層（ビジネスロジック層）
**場所**: `shop/services/`

**責務**:
- 複雑なビジネスロジック
- トランザクション処理
- 複数モデルにまたがる処理
- 再利用可能なロジック

**ファイル構成**:
```python
services/
├── __init__.py          # サービスのエクスポート
├── cart_service.py      # カート管理ロジック
└── order_service.py     # 注文管理ロジック
```

### 5. Form層（フォーム定義層）
**場所**: `shop/forms/`, `accounts/forms/`

**責務**:
- フォームの定義
- 入力値の検証
- ウィジェットのカスタマイズ

### 6. Admin層（管理画面層）
**場所**: `shop/admin/`, `accounts/admin.py`

**責務**:
- 管理画面の設定
- データの一覧・編集・削除機能
- カスタム管理アクション

### 7. Utility層（ユーティリティ層）
**場所**: `shop/utils/`

**責務**:
- 共通機能
- ヘルパー関数
- コンテキストプロセッサ

## 📊 データフロー

```
[HTTPリクエスト]
      ↓
[urls.py] → URLルーティング
      ↓
[View層] → リクエスト処理
      ↓
[Service層] → ビジネスロジック
      ↓
[Model層] → データベース操作
      ↓
[Template層] → HTML生成
      ↓
[HTTPレスポンス]
```

## 🎯 各層の役割と責任範囲

### Model層の責任
✅ すべきこと:
- データベーススキーマの定義
- フィールドのバリデーション
- プロパティメソッド（`@property`）
- `__str__`メソッド

❌ してはいけないこと:
- HTTPリクエスト・レスポンスの処理
- テンプレートのレンダリング
- 複雑なビジネスロジック

### View層の責任
✅ すべきこと:
- リクエストの受け取り
- 認証・認可のチェック
- Serviceの呼び出し
- テンプレートの選択とレンダリング

❌ してはいけないこと:
- 複雑なビジネスロジック
- 直接的なデータベース操作（単純なCRUD以外）

### Service層の責任
✅ すべきこと:
- ビジネスルールの実装
- トランザクション管理
- 複数モデルの操作
- データの加工・集計

❌ してはいけないこと:
- HTTPリクエスト・レスポンスの処理
- テンプレートのレンダリング

## 📝 命名規則

### ファイル名
- **モデル**: `<モデル名>.py` (例: `product.py`)
- **ビュー**: `<機能>_views.py` (例: `product_views.py`)
- **サービス**: `<機能>_service.py` (例: `cart_service.py`)
- **フォーム**: `<用途>_form.py` (例: `order_form.py`)
- **管理画面**: `<機能>_admin.py` (例: `product_admin.py`)

### クラス名
- **モデル**: `PascalCase` (例: `Product`, `OrderItem`)
- **ビュー**: `PascalCaseView` (例: `ProductListView`)
- **サービス**: `PascalCaseService` (例: `CartService`)
- **フォーム**: `PascalCaseForm` (例: `OrderForm`)
- **管理画面**: `PascalCaseAdmin` (例: `ProductAdmin`)

### 関数名
- **ビュー関数**: `snake_case` (例: `cart_view`, `add_to_cart`)
- **サービスメソッド**: `snake_case` (例: `get_or_create_cart`)

## 🔄 リファクタリングの利点

### Before（単一ファイル）
```python
shop/
├── models.py         # 500行以上
├── views.py          # 400行以上
├── forms.py          # 100行
└── admin.py          # 100行
```

### After（モジュール分割）
```python
shop/
├── models/           # 各50-100行
├── views/            # 各50-100行
├── services/         # 各50-150行
├── forms/            # 各30-50行
└── admin/            # 各30-60行
```

### メリット
1. **可読性の向上**: ファイルが小さく、目的が明確
2. **保守性の向上**: 修正箇所が特定しやすい
3. **テスタビリティ**: 各モジュールを独立してテスト可能
4. **拡張性**: 新機能追加が容易
5. **チーム開発**: 複数人での同時作業が容易

## 🧪 テスト構造（今後の実装）

```
tests/
├── models/
│   ├── test_product.py
│   ├── test_cart.py
│   └── test_order.py
├── views/
│   ├── test_product_views.py
│   ├── test_cart_views.py
│   └── test_order_views.py
└── services/
    ├── test_cart_service.py
    └── test_order_service.py
```

## 🚀 開発ワークフロー

### 新機能追加の手順

1. **Model作成**: `shop/models/<feature>.py`
2. **Service作成**: `shop/services/<feature>_service.py`
3. **Form作成**: `shop/forms/<feature>_form.py`
4. **View作成**: `shop/views/<feature>_views.py`
5. **Template作成**: `templates/shop/<feature>.html`
6. **Admin作成**: `shop/admin/<feature>_admin.py`
7. **URL追加**: `shop/urls.py`
8. **テスト作成**: `tests/<layer>/test_<feature>.py`

### 例: レビュー機能を追加する場合

```python
# 1. Model
shop/models/review.py

# 2. Service
shop/services/review_service.py

# 3. Form
shop/forms/review_form.py

# 4. View
shop/views/review_views.py

# 5. Template
templates/shop/review_list.html
templates/shop/review_form.html

# 6. Admin
shop/admin/review_admin.py
```

## 📚 参考資料

- Django公式ドキュメント: https://docs.djangoproject.com/
- MVCパターン: https://en.wikipedia.org/wiki/Model–view–controller
- クリーンアーキテクチャ: https://blog.cleancoder.com/
