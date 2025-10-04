# プロジェクト構造 - MVCアーキテクチャ

## 📁 フォルダ構成

```
pythonEC/
├── 📁 config/                    # プロジェクト設定
│   ├── __init__.py
│   ├── settings.py              # Django設定
│   ├── urls.py                  # ルートURLルーティング
│   ├── middleware.py            # カスタムミドルウェア（リクエスト/レスポンスロギング）
│   ├── wsgi.py                  # WSGIエントリーポイント
│   └── asgi.py                  # ASGIエントリーポイント
│
├── 📁 shop/                      # ECサイトメインアプリ
│   ├── 📁 models/               # 🗄️ MODEL層（データモデル）
│   │   ├── __init__.py          # モデルのエクスポート
│   │   ├── category.py          # カテゴリモデル
│   │   ├── product.py           # 商品モデル
│   │   ├── cart.py              # カート・カートアイテムモデル
│   │   └── order.py             # 注文・注文アイテムモデル
│   │
│   ├── 📁 views/                # 🎮 VIEW層（コントローラー）
│   │   ├── __init__.py          # ビューのエクスポート
│   │   ├── product_views.py    # 商品表示ビュー（一覧・詳細）
│   │   ├── cart_views.py       # カート操作ビュー（表示・追加・更新・削除）
│   │   └── order_views.py      # 注文処理ビュー（チェックアウト・履歴・詳細）
│   │
│   ├── 📁 services/             # 💼 SERVICE層（ビジネスロジック）
│   │   ├── __init__.py          # サービスのエクスポート
│   │   ├── cart_service.py     # カート管理ロジック（取得・作成・マージ）
│   │   └── order_service.py    # 注文管理ロジック（作成・キャンセル・ステータス更新）
│   │
│   ├── 📁 forms/                # 📝 FORM層（フォーム定義）
│   │   ├── __init__.py          # フォームのエクスポート
│   │   └── order_form.py       # 注文フォーム（配送先情報）
│   │
│   ├── 📁 admin/                # ⚙️ ADMIN層（管理画面）
│   │   ├── __init__.py          # 管理画面のエクスポート
│   │   ├── product_admin.py    # 商品・カテゴリ管理画面
│   │   ├── cart_admin.py       # カート管理画面（インライン）
│   │   └── order_admin.py      # 注文管理画面（インライン）
│   │
│   ├── 📁 utils/                # 🔧 UTILITY層（ユーティリティ）
│   │   ├── __init__.py
│   │   └── context_processors.py  # コンテキストプロセッサ（カート情報）
│   │
│   ├── 📁 migrations/           # データベースマイグレーション
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   │
│   ├── __init__.py
│   ├── apps.py                  # アプリ設定
│   └── urls.py                  # URLパターン
│
├── 📁 accounts/                  # ユーザー認証アプリ
│   ├── 📁 models/               # モデル層（現在は標準User使用）
│   │   └── __init__.py
│   │
│   ├── 📁 views/                # ビュー層
│   │   ├── __init__.py          # ビューのエクスポート
│   │   ├── auth_views.py       # 認証ビュー（ログイン・ログアウト・サインアップ）
│   │   └── profile_views.py    # プロフィールビュー
│   │
│   ├── 📁 forms/                # フォーム層
│   │   ├── __init__.py          # フォームのエクスポート
│   │   └── signup_form.py      # 登録フォーム（メール必須）
│   │
│   ├── __init__.py
│   ├── admin.py                 # 管理画面設定
│   ├── apps.py                  # アプリ設定
│   └── urls.py                  # URLパターン
│
├── 📁 templates/                 # 🎨 TEMPLATE層（ビュー）
│   ├── base.html                # ベーステンプレート（Bootstrap 5）
│   ├── 📁 shop/                 # ショップテンプレート
│   │   ├── product_list.html   # 商品一覧（ページネーション・カテゴリフィルタ）
│   │   ├── product_detail.html # 商品詳細
│   │   ├── cart.html            # カート表示
│   │   ├── checkout.html        # チェックアウト
│   │   ├── order_complete.html  # 注文完了
│   │   ├── order_history.html   # 注文履歴
│   │   └── order_detail.html    # 注文詳細
│   │
│   └── 📁 accounts/             # アカウントテンプレート
│       ├── login.html           # ログイン
│       ├── signup.html          # サインアップ
│       └── profile.html         # プロフィール
│
├── 📁 static/                    # 静的ファイル
│   └── 📁 css/
│       └── style.css            # カスタムスタイル
│
├── 📁 media/                     # アップロードファイル
│   └── 📁 products/             # 商品画像
│
├── 📁 design/                    # 📚 設計ドキュメント
│   ├── DESIGN.md                # システム設計書
│   ├── API_SPEC.md              # API仕様書（将来用）
│   ├── ARCHITECTURE.md          # アーキテクチャ設計書（本書）
│   └── OPERATION.md             # 運用マニュアル
│
├── 📁 tests/                     # 🧪 テストスイート
│   ├── __init__.py
│   ├── README.md                # テスト実行方法・構成説明
│   ├── test_integration.py      # 統合テスト（購入フロー等）
│   │
│   ├── 📁 shop/                 # ショップアプリのテスト
│   │   ├── __init__.py
│   │   ├── 📁 models/           # モデルテスト（33テスト）
│   │   │   ├── __init__.py
│   │   │   ├── test_category.py
│   │   │   ├── test_product.py
│   │   │   ├── test_cart.py
│   │   │   └── test_order.py
│   │   │
│   │   ├── 📁 services/         # サービステスト（14テスト）
│   │   │   ├── __init__.py
│   │   │   ├── test_cart_service.py
│   │   │   └── test_order_service.py
│   │   │
│   │   ├── � views/            # ビューテスト（24テスト）
│   │   │   ├── __init__.py
│   │   │   ├── test_product_views.py
│   │   │   ├── test_cart_views.py
│   │   │   └── test_order_views.py
│   │   │
│   │   └── 📁 forms/            # フォームテスト（6テスト）
│   │       ├── __init__.py
│   │       └── test_order_form.py
│   │
│   └── 📁 accounts/             # アカウントアプリのテスト
│       ├── __init__.py
│       ├── 📁 views/            # ビューテスト（9テスト）
│       │   ├── __init__.py
│       │   └── test_auth_views.py
│       │
│       └── 📁 forms/            # フォームテスト（8テスト）
│           ├── __init__.py
│           └── test_signup_form.py
│
├── �📄 manage.py                  # Django管理コマンド
├── 📄 requirements.txt           # Python依存関係
├── 📄 db.sqlite3                 # データベース（開発環境）
├── 📄 .gitignore                 # Git除外設定
├── 📄 README.md                  # プロジェクト概要
└── 📄 .coverage                  # カバレッジ測定結果
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

## 🧪 テスト構造（実装済み）

```
tests/                                    # 合計94テストケース
├── __init__.py
├── README.md                            # テスト実行方法・ドキュメント
├── test_integration.py                  # 統合テスト（7テスト）
│
├── shop/                                # ショップアプリテスト（77テスト）
│   ├── __init__.py
│   ├── models/                          # モデルテスト（33テスト）
│   │   ├── __init__.py
│   │   ├── test_category.py            # カテゴリ（5テスト）
│   │   ├── test_product.py             # 商品（7テスト）
│   │   ├── test_cart.py                # カート（12テスト）
│   │   └── test_order.py               # 注文（9テスト）
│   │
│   ├── services/                        # サービステスト（14テスト）
│   │   ├── __init__.py
│   │   ├── test_cart_service.py        # カートサービス（6テスト）
│   │   └── test_order_service.py       # 注文サービス（8テスト）
│   │
│   ├── views/                           # ビューテスト（24テスト）
│   │   ├── __init__.py
│   │   ├── test_product_views.py       # 商品ビュー（6テスト）
│   │   ├── test_cart_views.py          # カートビュー（8テスト）
│   │   └── test_order_views.py         # 注文ビュー（10テスト）
│   │
│   └── forms/                           # フォームテスト（6テスト）
│       ├── __init__.py
│       └── test_order_form.py          # 注文フォーム（6テスト）
│
└── accounts/                            # アカウントアプリテスト（17テスト）
    ├── __init__.py
    ├── views/                           # ビューテスト（9テスト）
    │   ├── __init__.py
    │   └── test_auth_views.py          # 認証ビュー（9テスト）
    │
    └── forms/                           # フォームテスト（8テスト）
        ├── __init__.py
        └── test_signup_form.py         # サインアップフォーム（8テスト）
```

### テスト実行方法

```bash
# すべてのテストを実行
python manage.py test

# 特定のレイヤーのテストを実行
python manage.py test tests.shop.models
python manage.py test tests.shop.services
python manage.py test tests.shop.views

# カバレッジ測定
coverage run --source='.' manage.py test
coverage report
coverage html
```

### テストカバレッジ

- **モデル層**: 100% - オブジェクト作成、プロパティ、制約をすべてテスト
- **サービス層**: 100% - ビジネスロジック、トランザクション処理を網羅
- **ビュー層**: 95%以上 - HTTPリクエスト/レスポンス、認証を確認
- **フォーム層**: 100% - バリデーション、ウィジェット属性を検証
- **統合テスト**: 完全な購入フロー、ゲストカート移行を実装

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

## �️ 実装済み機能

### コア機能
- ✅ ユーザー認証（ログイン・ログアウト・サインアップ）
- ✅ 商品管理（カテゴリ・商品CRUD）
- ✅ カート機能（ゲスト・ユーザーカート、マージ機能）
- ✅ 注文処理（チェックアウト・注文履歴・詳細表示）
- ✅ 在庫管理（注文時減算、キャンセル時復元）
- ✅ 管理画面（商品・カート・注文管理）

### 開発支援機能
- ✅ リクエスト/レスポンスロギングミドルウェア
- ✅ コンテキストプロセッサ（カート情報グローバル表示）
- ✅ 包括的なテストスイート（94テストケース）
- ✅ カバレッジ測定環境

### UI/UX
- ✅ レスポンシブデザイン（Bootstrap 5）
- ✅ ページネーション（商品一覧）
- ✅ カテゴリフィルタリング
- ✅ カート数量表示（ナビゲーションバー）

## 🔧 主要なサービスクラス

### CartService
**場所**: `shop/services/cart_service.py`

**メソッド**:
- `get_or_create_cart(request)` - カートの取得または作成（ユーザー/ゲスト対応）
- `merge_guest_cart_to_user(request, user)` - ゲストカートをユーザーカートにマージ
- `clear_cart(cart)` - カートの全商品削除

### OrderService
**場所**: `shop/services/order_service.py`

**メソッド**:
- `create_order_from_cart(user, cart, shipping_data)` - カートから注文を作成
- `cancel_order(order)` - 注文キャンセル（在庫復元）
- `update_order_status(order, status)` - 注文ステータス更新

## 🔐 セキュリティ実装

### 認証・認可
- ✅ `@login_required` デコレータ（チェックアウト、注文履歴等）
- ✅ オーナーチェック（他ユーザーの注文閲覧不可）
- ✅ パスワードのログ出力時マスキング

### データ保護
- ✅ CSRF保護（Django標準）
- ✅ SQLインジェクション対策（ORM使用）
- ✅ XSS対策（テンプレート自動エスケープ）

## 📊 パフォーマンス最適化

### データベース
- ✅ `select_related()` - 外部キー関連の最適化
- ✅ `prefetch_related()` - 多対多関連の最適化
- ✅ インデックス（slug, created_at等）

### キャッシング（今後実装予定）
- ⏳ 商品一覧のキャッシュ
- ⏳ カテゴリ一覧のキャッシュ
- ⏳ Redis導入

## 🚧 今後の拡張予定

### 機能拡張
- ⏳ レビュー機能
- ⏳ お気に入り機能
- ⏳ クーポン機能
- ⏳ ポイントシステム
- ⏳ メール通知（注文確認、発送通知）
- ⏳ 決済機能統合（Stripe等）

### API開発
- ⏳ REST API（Django REST Framework）
- ⏳ GraphQL API
- ⏳ フロントエンド分離（React/Vue.js）

### インフラ
- ⏳ PostgreSQL移行
- ⏳ Redis導入
- ⏳ Docker化
- ⏳ CI/CD パイプライン

## �📚 参考資料

- Django公式ドキュメント: https://docs.djangoproject.com/
- MVCパターン: https://en.wikipedia.org/wiki/Model–view–controller
- クリーンアーキテクチャ: https://blog.cleancoder.com/
- Django Testing: https://docs.djangoproject.com/en/stable/topics/testing/

---

**最終更新日**: 2025年10月4日  
**バージョン**: 1.1  
**ステータス**: 基本機能実装完了、テストスイート完備
