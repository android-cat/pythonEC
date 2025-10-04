# ECサイト API仕様書

## 概要

このドキュメントは、DjangoベースのECサイトのAPI仕様を定義します。
現在はテンプレートベースのWebアプリケーションですが、将来的なREST API化を見据えた設計です。

---

## エンドポイント一覧

### 商品API

#### 商品一覧取得
```
GET /api/products/
```

**クエリパラメータ**:
- `category` (optional): カテゴリスラッグでフィルター
- `page` (optional): ページ番号
- `per_page` (optional): 1ページあたりの件数

**レスポンス例**:
```json
{
  "count": 50,
  "next": "/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "ノートPC",
      "slug": "notebook-pc",
      "category": {
        "id": 1,
        "name": "電子機器",
        "slug": "electronics"
      },
      "description": "高性能ノートパソコン",
      "price": "89800",
      "stock": 10,
      "image": "/media/products/laptop.jpg",
      "is_active": true,
      "created_at": "2025-10-01T10:00:00Z",
      "updated_at": "2025-10-01T10:00:00Z"
    }
  ]
}
```

#### 商品詳細取得
```
GET /api/products/<slug>/
```

**レスポンス例**:
```json
{
  "id": 1,
  "name": "ノートPC",
  "slug": "notebook-pc",
  "category": {
    "id": 1,
    "name": "電子機器",
    "slug": "electronics"
  },
  "description": "高性能ノートパソコン",
  "price": "89800",
  "stock": 10,
  "image": "/media/products/laptop.jpg",
  "is_active": true,
  "is_in_stock": true,
  "created_at": "2025-10-01T10:00:00Z",
  "updated_at": "2025-10-01T10:00:00Z"
}
```

### カートAPI

#### カート取得
```
GET /api/cart/
```

**認証**: 任意（ログインユーザーはuser_id、ゲストはsession_keyで識別）

**レスポンス例**:
```json
{
  "id": 1,
  "user": 1,
  "session_key": null,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "ノートPC",
        "price": "89800",
        "image": "/media/products/laptop.jpg"
      },
      "quantity": 2,
      "subtotal": "179600"
    }
  ],
  "total_price": "179600",
  "total_items": 2,
  "created_at": "2025-10-01T10:00:00Z",
  "updated_at": "2025-10-01T12:00:00Z"
}
```

#### カートに商品追加
```
POST /api/cart/items/
```

**リクエストボディ**:
```json
{
  "product_id": 1,
  "quantity": 1
}
```

**レスポンス**:
```json
{
  "id": 1,
  "cart": 1,
  "product": {
    "id": 1,
    "name": "ノートPC",
    "price": "89800"
  },
  "quantity": 1,
  "subtotal": "89800"
}
```

#### カート商品更新
```
PATCH /api/cart/items/<item_id>/
```

**リクエストボディ**:
```json
{
  "quantity": 3
}
```

#### カート商品削除
```
DELETE /api/cart/items/<item_id>/
```

### 注文API

#### 注文作成（チェックアウト）
```
POST /api/orders/
```

**認証**: 必須

**リクエストボディ**:
```json
{
  "shipping_name": "山田太郎",
  "shipping_postal_code": "123-4567",
  "shipping_address": "東京都渋谷区...",
  "shipping_phone": "090-1234-5678"
}
```

**レスポンス**:
```json
{
  "id": 1,
  "user": 1,
  "status": "pending",
  "total_amount": "179600",
  "shipping_name": "山田太郎",
  "shipping_postal_code": "123-4567",
  "shipping_address": "東京都渋谷区...",
  "shipping_phone": "090-1234-5678",
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "ノートPC"
      },
      "quantity": 2,
      "price": "89800",
      "subtotal": "179600"
    }
  ],
  "created_at": "2025-10-01T15:00:00Z"
}
```

#### 注文履歴取得
```
GET /api/orders/
```

**認証**: 必須

**レスポンス**:
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "status": "delivered",
      "total_amount": "179600",
      "created_at": "2025-10-01T15:00:00Z"
    }
  ]
}
```

#### 注文詳細取得
```
GET /api/orders/<order_id>/
```

**認証**: 必須

### 認証API

#### ユーザー登録
```
POST /api/accounts/signup/
```

**リクエストボディ**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password1": "securepassword123",
  "password2": "securepassword123"
}
```

#### ログイン
```
POST /api/accounts/login/
```

**リクエストボディ**:
```json
{
  "username": "testuser",
  "password": "securepassword123"
}
```

**レスポンス**:
```json
{
  "token": "abc123...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

#### ログアウト
```
POST /api/accounts/logout/
```

**認証**: 必須

---

## エラーレスポンス

### 400 Bad Request
```json
{
  "error": "validation_error",
  "message": "入力内容に誤りがあります",
  "details": {
    "quantity": ["この値は0より大きくなければなりません"]
  }
}
```

### 401 Unauthorized
```json
{
  "error": "authentication_required",
  "message": "ログインが必要です"
}
```

### 403 Forbidden
```json
{
  "error": "permission_denied",
  "message": "この操作を実行する権限がありません"
}
```

### 404 Not Found
```json
{
  "error": "not_found",
  "message": "リソースが見つかりません"
}
```

### 500 Internal Server Error
```json
{
  "error": "server_error",
  "message": "サーバーエラーが発生しました"
}
```

---

## 認証方式

### セッション認証（現在の実装）
- DjangoのセッションベースCookie認証
- CSRFトークンによる保護

### トークン認証（将来的な実装）
- JWT（JSON Web Token）
- Authorization Header: `Bearer <token>`

---

## レート制限

将来的な実装:
- 認証済みユーザー: 100リクエスト/分
- 匿名ユーザー: 20リクエスト/分

---

## バージョニング

将来的なAPI実装時:
- URLバージョニング: `/api/v1/products/`
- Headerバージョニング: `Accept: application/json; version=1.0`
