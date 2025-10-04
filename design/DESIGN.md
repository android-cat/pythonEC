# ECサイト設計書

## プロジェクト概要

DjangoのMTV（Model-Template-View）パターンで構築されたEコマースサイト。
商品の閲覧、カート機能、注文管理、ユーザー認証機能を備えています。

### 技術スタック
- **フレームワーク**: Django 4.2+
- **データベース**: SQLite3（開発環境）
- **フロントエンド**: Bootstrap 5, HTML5, CSS3
- **画像処理**: Pillow

---

## システム構成

### アプリケーション構成

```
pythonEC/
├── config/              # プロジェクト設定
│   ├── settings.py     # Django設定
│   ├── urls.py         # URLルーティング
│   ├── middleware.py   # カスタムミドルウェア
│   └── wsgi.py         # WSGIエントリーポイント
├── shop/               # ECサイトメインアプリ
│   ├── models.py       # 商品・カート・注文モデル
│   ├── views.py        # ビュー処理
│   ├── urls.py         # URLパターン
│   ├── forms.py        # フォーム定義
│   ├── admin.py        # 管理画面設定
│   └── context_processors.py  # コンテキストプロセッサ
├── accounts/           # ユーザー認証アプリ
│   ├── models.py       # ユーザーモデル
│   ├── views.py        # 認証ビュー
│   ├── urls.py         # URLパターン
│   └── forms.py        # 認証フォーム
├── templates/          # HTMLテンプレート
│   ├── base.html       # ベーステンプレート
│   ├── shop/           # ショップテンプレート
│   └── accounts/       # アカウントテンプレート
├── static/             # 静的ファイル
│   └── css/
│       └── style.css
└── media/              # アップロードファイル
```

---

## データベース設計

### ER図（概念図）

```
User (Django標準)
  ↓ 1:N
Order ← 1:N → OrderItem → N:1 → Product → N:1 → Category
  ↑
  |
Cart ← 1:N → CartItem → N:1 → Product
```

### テーブル定義

#### 1. Category（カテゴリ）

| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | BigInteger | PK | 主キー |
| name | VARCHAR(100) | NOT NULL | カテゴリ名 |
| slug | VARCHAR(50) | UNIQUE, NOT NULL | URLスラッグ |
| description | TEXT | NULL | 説明 |
| created_at | DateTime | NOT NULL | 作成日時 |
| updated_at | DateTime | NOT NULL | 更新日時 |

**インデックス**: slug

#### 2. Product（商品）

| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | BigInteger | PK | 主キー |
| name | VARCHAR(200) | NOT NULL | 商品名 |
| slug | VARCHAR(50) | UNIQUE, NOT NULL | URLスラッグ |
| category_id | BigInteger | FK(Category) | カテゴリID |
| description | TEXT | NOT NULL | 商品説明 |
| price | Decimal(10,0) | NOT NULL | 価格 |
| stock | Integer | NOT NULL, DEFAULT 0 | 在庫数 |
| image | VARCHAR(100) | NULL | 画像パス |
| is_active | Boolean | NOT NULL, DEFAULT TRUE | 販売中フラグ |
| created_at | DateTime | NOT NULL | 作成日時 |
| updated_at | DateTime | NOT NULL | 更新日時 |

**インデックス**: slug, category_id, is_active

#### 3. Cart（カート）

| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | BigInteger | PK | 主キー |
| user_id | Integer | FK(User), NULL | ユーザーID |
| session_key | VARCHAR(40) | NULL | セッションキー |
| created_at | DateTime | NOT NULL | 作成日時 |
| updated_at | DateTime | NOT NULL | 更新日時 |

**インデックス**: user_id, session_key

**注意**: ログインユーザーは`user_id`、ゲストは`session_key`で識別

#### 4. CartItem（カート商品）

| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | BigInteger | PK | 主キー |
| cart_id | BigInteger | FK(Cart) | カートID |
| product_id | BigInteger | FK(Product) | 商品ID |
| quantity | Integer | NOT NULL, DEFAULT 1 | 数量 |
| created_at | DateTime | NOT NULL | 作成日時 |
| updated_at | DateTime | NOT NULL | 更新日時 |

**ユニーク制約**: (cart_id, product_id)

#### 5. Order（注文）

| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | BigInteger | PK | 主キー |
| user_id | Integer | FK(User) | ユーザーID |
| status | VARCHAR(20) | NOT NULL | ステータス |
| total_amount | Decimal(10,0) | NOT NULL | 合計金額 |
| shipping_name | VARCHAR(100) | NOT NULL | 配送先氏名 |
| shipping_postal_code | VARCHAR(10) | NOT NULL | 郵便番号 |
| shipping_address | TEXT | NOT NULL | 住所 |
| shipping_phone | VARCHAR(20) | NOT NULL | 電話番号 |
| created_at | DateTime | NOT NULL | 注文日時 |
| updated_at | DateTime | NOT NULL | 更新日時 |

**ステータス値**:
- `pending`: 注文受付
- `processing`: 処理中
- `shipped`: 発送済み
- `delivered`: 配達完了
- `cancelled`: キャンセル

**インデックス**: user_id, status, created_at

#### 6. OrderItem（注文商品）

| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | BigInteger | PK | 主キー |
| order_id | BigInteger | FK(Order) | 注文ID |
| product_id | BigInteger | FK(Product) | 商品ID |
| quantity | Integer | NOT NULL | 数量 |
| price | Decimal(10,0) | NOT NULL | 単価（注文時点） |

**インデックス**: order_id

---

## 機能仕様

### 1. 商品管理機能

#### 1.1 商品一覧表示
- **URL**: `/` または `/category/<category_slug>/`
- **View**: `ProductListView`
- **Template**: `shop/product_list.html`
- **機能**:
  - 全商品またはカテゴリ別の商品一覧を表示
  - ページネーション（12件/ページ）
  - 販売中（is_active=True）の商品のみ表示
  - カテゴリフィルター

#### 1.2 商品詳細表示
- **URL**: `/product/<slug>/`
- **View**: `ProductDetailView`
- **Template**: `shop/product_detail.html`
- **機能**:
  - 商品の詳細情報を表示
  - 在庫状況の表示
  - カートへの追加ボタン

### 2. カート機能

#### 2.1 カート表示
- **URL**: `/cart/`
- **View**: `cart_view`
- **Template**: `shop/cart.html`
- **機能**:
  - カート内の商品一覧を表示
  - 合計金額・商品数の計算
  - 数量変更・削除機能

#### 2.2 カートに追加
- **URL**: `/cart/add/<product_id>/`
- **View**: `add_to_cart`
- **処理**:
  1. カートを取得または作成
  2. CartItemを作成または数量を+1
  3. メッセージを表示してカート画面へリダイレクト

#### 2.3 カート商品の更新
- **URL**: `/cart/update/<item_id>/`
- **View**: `update_cart_item`
- **処理**:
  - 数量を指定された値に更新
  - 数量が0以下の場合は削除

#### 2.4 カートから削除
- **URL**: `/cart/remove/<item_id>/`
- **View**: `remove_from_cart`
- **処理**:
  - CartItemを削除

### 3. 注文機能

#### 3.1 チェックアウト
- **URL**: `/checkout/`
- **View**: `checkout`
- **Template**: `shop/checkout.html`
- **認証**: ログイン必須
- **処理フロー**:
  1. カートが空でないことを確認
  2. 配送先情報フォームを表示
  3. フォーム送信時:
     - Orderを作成
     - OrderItemを作成
     - 在庫を減少
     - カートをクリア
     - 注文完了画面へリダイレクト

#### 3.2 注文完了
- **URL**: `/order/complete/<order_id>/`
- **View**: `order_complete`
- **Template**: `shop/order_complete.html`
- **機能**:
  - 注文確認情報の表示

#### 3.3 注文履歴
- **URL**: `/orders/`
- **View**: `order_history`
- **Template**: `shop/order_history.html`
- **認証**: ログイン必須
- **機能**:
  - ユーザーの注文一覧を表示

#### 3.4 注文詳細
- **URL**: `/order/<order_id>/`
- **View**: `order_detail`
- **Template**: `shop/order_detail.html`
- **認証**: ログイン必須
- **機能**:
  - 注文の詳細情報を表示

### 4. ユーザー認証機能

#### 4.1 ユーザー登録
- **URL**: `/accounts/signup/`
- **View**: `signup`
- **Template**: `accounts/signup.html`
- **機能**:
  - 新規ユーザー登録
  - 登録後自動ログイン

#### 4.2 ログイン
- **URL**: `/accounts/login/`
- **View**: `CustomLoginView`
- **Template**: `accounts/login.html`
- **機能**:
  - ユーザー名とパスワードで認証
  - ログイン後、元のページまたはトップページへリダイレクト

#### 4.3 ログアウト
- **URL**: `/accounts/logout/`
- **View**: Django標準`LogoutView`
- **処理**:
  - ログアウト後、トップページへリダイレクト

#### 4.4 プロフィール
- **URL**: `/accounts/profile/`
- **View**: `profile`
- **Template**: `accounts/profile.html`
- **認証**: ログイン必須
- **機能**:
  - ユーザー情報の表示
  - 最近の注文履歴（5件）

### 5. 管理機能

#### 5.1 Django管理画面
- **URL**: `/admin/`
- **機能**:
  - カテゴリ管理
  - 商品管理（在庫・価格編集）
  - 注文管理（ステータス変更）
  - カート確認
  - ユーザー管理

---

## URL設計

### Shop アプリ

| URL | View | 名前 | 説明 |
|-----|------|------|------|
| `/` | ProductListView | product_list | 商品一覧 |
| `/category/<slug:category_slug>/` | ProductListView | product_list_by_category | カテゴリ別商品一覧 |
| `/product/<slug:slug>/` | ProductDetailView | product_detail | 商品詳細 |
| `/cart/` | cart_view | cart | カート表示 |
| `/cart/add/<int:product_id>/` | add_to_cart | add_to_cart | カートに追加 |
| `/cart/update/<int:item_id>/` | update_cart_item | update_cart_item | カート更新 |
| `/cart/remove/<int:item_id>/` | remove_from_cart | remove_from_cart | カートから削除 |
| `/checkout/` | checkout | checkout | チェックアウト |
| `/order/complete/<int:order_id>/` | order_complete | order_complete | 注文完了 |
| `/orders/` | order_history | order_history | 注文履歴 |
| `/order/<int:order_id>/` | order_detail | order_detail | 注文詳細 |

### Accounts アプリ

| URL | View | 名前 | 説明 |
|-----|------|------|------|
| `/accounts/login/` | CustomLoginView | login | ログイン |
| `/accounts/logout/` | LogoutView | logout | ログアウト |
| `/accounts/signup/` | signup | signup | ユーザー登録 |
| `/accounts/profile/` | profile | profile | プロフィール |

---

## ビジネスロジック

### カート処理

#### ゲストユーザーとログインユーザーの切り替え

```python
def get_or_create_cart(request):
    if request.user.is_authenticated:
        # ログインユーザー: user_idで識別
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # ゲストユーザー: session_keyで識別
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart
```

### 注文処理フロー

1. **チェックアウト開始**
   - カートが空でないことを確認
   - ログインチェック（未ログインの場合はログインページへ）

2. **配送先情報入力**
   - OrderFormで配送先情報を入力

3. **注文作成**
   ```python
   - Order作成（ユーザー、合計金額、配送先情報）
   - カート内の各商品についてOrderItem作成
   - 在庫を減算: product.stock -= item.quantity
   - カートをクリア: cart.items.all().delete()
   ```

4. **注文完了**
   - 注文番号を表示
   - 注文詳細を表示

### 在庫管理

- **在庫チェック**: `product.is_in_stock` プロパティ
- **在庫減算**: 注文確定時に実行
- **在庫表示**: 商品詳細・一覧で在庫状況を表示

---

## セキュリティ対策

### 1. CSRF対策
- すべてのPOSTリクエストに`{% csrf_token %}`を使用
- DjangoのCSRFミドルウェアが有効

### 2. 認証・認可
- ログイン必須ページ: `@login_required`デコレータ
- 注文詳細: 自分の注文のみ表示可能

### 3. SQLインジェクション対策
- Django ORMを使用（パラメータ化されたクエリ）

### 4. XSS対策
- テンプレートで自動エスケープ有効

### 5. パスワード管理
- Django標準のパスワードハッシュ化
- パスワード検証ルール適用

---

## コンテキストプロセッサ

### cart_context

全てのテンプレートでカート情報を利用可能にする。

```python
def cart_context(request):
    return {
        'cart': cart,
        'cart_total_items': cart.total_items if cart else 0,
    }
```

**利用例**: ナビゲーションバーにカート内商品数を表示

---

## ミドルウェア

### RequestResponseLoggingMiddleware

リクエストとレスポンスのログを記録（デバッグ用）。

**ログ内容**:
- HTTPメソッド、パス
- ユーザー情報、認証状態
- POSTデータ（パスワードは隠蔽）
- レスポンスステータス、リダイレクト先

---

## フォーム定義

### OrderForm
- 配送先情報の入力フォーム
- Bootstrapクラスを適用

### SignUpForm
- ユーザー登録フォーム
- Django標準UserCreationFormを継承
- メールアドレスフィールドを追加

---

## テンプレート構成

### ベーステンプレート（base.html）

全ページで共通のレイアウト:
- ナビゲーションバー
- メッセージ表示エリア
- フッター
- Bootstrap 5読み込み

### ブロック定義
- `{% block title %}`: ページタイトル
- `{% block content %}`: メインコンテンツ
- `{% block extra_css %}`: 追加CSS
- `{% block extra_js %}`: 追加JavaScript

---

## 画面遷移図

```
[商品一覧] ─→ [商品詳細] ─→ [カートに追加]
    ↓                           ↓
[カテゴリ別]                  [カート]
                                ↓
                         [チェックアウト] ※要ログイン
                                ↓
                           [注文完了]
                                ↓
                           [注文履歴]
                                ↓
                           [注文詳細]

[ログイン] ←→ [新規登録]
    ↓
[プロフィール]
```

---

## 開発環境セットアップ

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. データベース初期化
```bash
# マイグレーション作成
python manage.py makemigrations

# マイグレーション適用
python manage.py migrate
```

### 3. スーパーユーザー作成
```bash
python manage.py createsuperuser
```

### 4. 開発サーバー起動
```bash
python manage.py runserver
```

### 5. 初期データ登録

管理画面（http://localhost:8000/admin/）からカテゴリと商品を登録。

---

## テストデータ作成例

### カテゴリ
- 電子機器 (slug: electronics)
- 書籍 (slug: books)
- 衣料品 (slug: clothing)

### 商品例
```python
商品名: ノートPC
カテゴリ: 電子機器
価格: 89800
在庫: 10
説明: 高性能ノートパソコン
```

---

## 今後の拡張案

### 機能追加
1. **検索機能**: 商品名・説明で検索
2. **レビュー機能**: 商品レビュー・評価
3. **お気に入り機能**: 商品をお気に入りに追加
4. **決済機能**: Stripe等の決済サービス連携
5. **メール通知**: 注文確認メール送信
6. **クーポン機能**: 割引クーポン
7. **商品画像ギャラリー**: 複数画像対応
8. **在庫アラート**: 在庫切れ通知

### パフォーマンス改善
1. **キャッシュ**: Redis/Memcachedでキャッシュ
2. **画像最適化**: サムネイル生成
3. **CDN**: 静的ファイル配信
4. **データベース最適化**: インデックス追加

### セキュリティ強化
1. **レート制限**: ログイン試行回数制限
2. **2段階認証**: SMS/アプリ認証
3. **HTTPS**: SSL/TLS対応

---

## トラブルシューティング

### 問題: マイグレーションエラー
```bash
# マイグレーションをリセット
python manage.py migrate --fake shop zero
python manage.py migrate --fake accounts zero
python manage.py migrate
```

### 問題: 静的ファイルが読み込まれない
```bash
# 静的ファイルを収集
python manage.py collectstatic
```

### 問題: 管理画面でログインできない
- ユーザー名（メールではない）でログイン
- パスワードをリセット: `python manage.py changepassword <username>`

---

## ライセンス

MIT License

---

## 作成日
2025年10月4日
