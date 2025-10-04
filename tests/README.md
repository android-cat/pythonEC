# テストスイート

このディレクトリには、Django ECサイトプロジェクトの包括的なテストスイートが含まれています。

## テスト構成

```
tests/
├── __init__.py                      # テストパッケージ初期化
├── test_integration.py              # 統合テスト
├── shop/                            # ショップアプリのテスト
│   ├── models/                      # モデルレイヤーテスト
│   │   ├── test_category.py        # カテゴリモデル (5テスト)
│   │   ├── test_product.py         # 商品モデル (7テスト)
│   │   ├── test_cart.py            # カート/カートアイテムモデル (12テスト)
│   │   └── test_order.py           # 注文/注文アイテムモデル (9テスト)
│   ├── services/                    # サービスレイヤーテスト
│   │   ├── test_cart_service.py    # カートサービス (6テスト)
│   │   └── test_order_service.py   # 注文サービス (8テスト)
│   ├── views/                       # ビューレイヤーテスト
│   │   ├── test_product_views.py   # 商品ビュー (6テスト)
│   │   ├── test_cart_views.py      # カートビュー (8テスト)
│   │   └── test_order_views.py     # 注文ビュー (10テスト)
│   └── forms/                       # フォームレイヤーテスト
│       └── test_order_form.py      # 注文フォーム (6テスト)
└── accounts/                        # アカウントアプリのテスト
    ├── views/                       # ビューレイヤーテスト
    │   └── test_auth_views.py      # 認証ビュー (9テスト)
    └── forms/                       # フォームレイヤーテスト
        └── test_signup_form.py     # サインアップフォーム (8テスト)
```

## テスト統計

- **合計テストケース数**: 94テスト
  - モデルテスト: 33
  - サービステスト: 14
  - ビューテスト: 33
  - フォームテスト: 14
  - 統合テスト: 7 (test_integration.py内)

## テストの実行方法

### すべてのテストを実行
```bash
python manage.py test
```

### 特定のアプリのテストを実行
```bash
# ショップアプリのテストのみ
python manage.py test tests.shop

# アカウントアプリのテストのみ
python manage.py test tests.accounts
```

### 特定のテストモジュールを実行
```bash
# モデルテストのみ
python manage.py test tests.shop.models

# サービステストのみ
python manage.py test tests.shop.services

# ビューテストのみ
python manage.py test tests.shop.views

# 統合テストのみ
python manage.py test tests.test_integration
```

### 特定のテストケースを実行
```bash
# 商品モデルのテストのみ
python manage.py test tests.shop.models.test_product

# カートサービスのテストのみ
python manage.py test tests.shop.services.test_cart_service

# 特定のテストメソッドのみ
python manage.py test tests.shop.models.test_product.ProductModelTest.test_product_creation
```

### 詳細な出力でテストを実行
```bash
python manage.py test --verbosity=2
```

### カバレッジ付きでテストを実行
```bash
# coverageをインストール
pip install coverage

# カバレッジ測定でテストを実行
coverage run --source='.' manage.py test

# カバレッジレポートを表示
coverage report

# HTML形式でカバレッジレポートを生成
coverage html
```

## テスト内容

### 1. モデルレイヤーテスト (tests/shop/models/)

**test_category.py** - カテゴリモデル
- オブジェクト作成
- 文字列表現 (`__str__`)
- スラッグの一意性制約
- 作成日時の自動設定
- 名前順での並び替え

**test_product.py** - 商品モデル
- オブジェクト作成
- 文字列表現
- `is_in_stock`プロパティ（在庫状況）
- スラッグの一意性制約
- 作成日時・更新日時の自動設定
- デフォルト値（在庫数0）
- 作成日時降順での並び替え

**test_cart.py** - カート/カートアイテムモデル
- ユーザーカートとゲストカートの作成
- 文字列表現
- `total_price`プロパティ
- `total_items`プロパティ
- カートアイテムの`subtotal`プロパティ
- `unique_together`制約（カート+商品）

**test_order.py** - 注文/注文アイテムモデル
- オブジェクト作成
- 文字列表現
- ステータス選択肢
- 注文アイテムの価格スナップショット
- 作成日時の自動設定

### 2. サービスレイヤーテスト (tests/shop/services/)

**test_cart_service.py** - カートサービス
- 認証済みユーザーのカート取得/作成
- ゲストユーザーのカート取得/作成
- カートクリア機能
- ゲストカートからユーザーカートへのマージ
- 既存カートへの商品追加時の数量加算

**test_order_service.py** - 注文サービス
- カートから注文を作成
- 合計金額の計算
- 在庫の減算
- 注文キャンセル機能
- 在庫の復元
- ステータス更新機能
- 無効なステータスでのエラー処理

### 3. ビューレイヤーテスト (tests/shop/views/)

**test_product_views.py** - 商品ビュー
- 商品一覧表示
- ページネーション（1ページ12商品）
- カテゴリフィルタリング
- 商品詳細表示
- 404エラー処理

**test_cart_views.py** - カートビュー
- カート表示
- カートに商品追加
- 既存商品の数量増加
- カートアイテム数量更新
- カートから商品削除

**test_order_views.py** - 注文ビュー
- チェックアウトページ表示
- ログイン要件
- 空のカートでのリダイレクト
- 注文作成
- 注文履歴表示
- 自分の注文のみ表示
- 注文詳細表示
- 他ユーザーの注文へのアクセス拒否

### 4. フォームレイヤーテスト (tests/shop/forms/ & tests/accounts/forms/)

**test_order_form.py** - 注文フォーム
- 正しいデータでのバリデーション
- 必須フィールドのバリデーション
- ウィジェット属性（CSSクラス、プレースホルダー）

**test_signup_form.py** - サインアップフォーム
- 正しいデータでのバリデーション
- メールアドレス必須
- メール形式バリデーション
- パスワード一致チェック
- ユーザー名重複チェック
- ユーザー保存機能
- ウィジェット属性

### 5. 認証ビューテスト (tests/accounts/views/)

**test_auth_views.py** - 認証関連ビュー
- ログインページ表示
- 正しい認証情報でのログイン
- 無効な認証情報での失敗
- ログアウト機能（GET/POST）
- サインアップページ表示
- サインアップでのユーザー作成
- 自動ログイン
- ユーザー名重複エラー
- プロフィールページ表示
- ログイン要件

### 6. 統合テスト (tests/test_integration.py)

**test_integration.py** - エンドツーエンドフロー
- 完全な購入フロー
  1. ログイン
  2. 商品一覧表示
  3. 商品詳細表示
  4. カートに追加
  5. カート表示
  6. チェックアウト
  7. 注文作成
  8. 注文履歴確認
  9. 注文詳細確認
- ゲストカートからユーザーカートへの移行
- カート数量更新フロー
- カートから削除フロー
- 空カートでのチェックアウト拒否
- 合計金額計算の正確性

## テスト設計思想

このテストスイートは、以下の原則に基づいて設計されています：

1. **レイヤー分離**: モデル、サービス、ビュー、フォームを個別にテスト
2. **独立性**: 各テストは他のテストに依存せず独立して実行可能
3. **包括性**: 正常系と異常系の両方をカバー
4. **実用性**: 実際のユーザーフローを統合テストで検証
5. **保守性**: テストコードも本番コードと同様に品質を重視

## テストデータ

各テストは`setUp()`メソッドでテストデータを初期化し、テスト後に自動的にクリーンアップされます。
テストデータベースは本番データベースとは別に管理されます。

## カバレッジ目標

- モデル: 100%
- サービス: 100%
- ビュー: 90%以上
- フォーム: 100%

## 今後の拡張

- パフォーマンステスト
- セキュリティテスト
- UIテスト（Selenium）
- API テスト（将来のREST API実装時）
