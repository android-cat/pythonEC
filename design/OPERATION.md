# ECサイト 運用マニュアル

## 目次
1. [日常運用](#日常運用)
2. [商品管理](#商品管理)
3. [注文管理](#注文管理)
4. [ユーザー管理](#ユーザー管理)
5. [バックアップ](#バックアップ)
6. [トラブルシューティング](#トラブルシューティング)

---

## 日常運用

### 管理画面へのアクセス

1. ブラウザで管理画面URLにアクセス
   ```
   http://localhost:8000/admin/
   ```

2. 管理者アカウントでログイン
   - ユーザー名: `admin`（または作成したユーザー名）
   - パスワード: 設定したパスワード

### ダッシュボード確認

管理画面トップで以下を確認:
- 最近追加された商品
- 最近の注文
- ユーザー登録状況

---

## 商品管理

### 商品の追加

1. 管理画面で「商品」→「商品を追加」をクリック

2. 必須項目を入力:
   - **商品名**: 商品の名称
   - **スラッグ**: URL用（例: `product-name`）
   - **カテゴリ**: プルダウンから選択
   - **説明**: 商品の詳細説明
   - **価格**: 数値のみ（例: 1980）
   - **在庫数**: 現在の在庫数
   - **販売中**: チェックを入れると公開

3. 任意項目:
   - **画像**: 商品画像をアップロード

4. 「保存」をクリック

### 商品の編集

1. 管理画面で「商品」→編集したい商品をクリック

2. 項目を修正

3. 「保存」をクリック

### 在庫管理

#### 在庫数の更新
1. 商品一覧画面で在庫数を直接編集可能
2. 複数商品の在庫を一括更新できます

#### 在庫切れ対応
- 在庫が0になると自動的に「在庫切れ」表示
- 「販売中」チェックを外すと商品一覧から非表示

### 商品の削除

1. 商品詳細ページで「削除」ボタン
2. 確認画面で「はい、削除します」をクリック

**注意**: 注文履歴に含まれる商品は削除できません

---

## カテゴリ管理

### カテゴリの追加

1. 管理画面で「カテゴリ」→「カテゴリを追加」

2. 入力項目:
   - **カテゴリ名**: カテゴリの名称
   - **スラッグ**: URL用（自動生成可）
   - **説明**: カテゴリの説明（任意）

3. 「保存」をクリック

### カテゴリの並び替え

カテゴリは名前順（50音順）で自動ソートされます。

---

## 注文管理

### 新規注文の確認

1. 管理画面で「注文」をクリック

2. 新しい注文は「注文受付」ステータスで表示

3. 注文詳細を確認:
   - 注文番号
   - 注文者情報
   - 配送先情報
   - 注文商品と数量
   - 合計金額

### 注文ステータスの更新

注文一覧画面でステータスを直接変更可能:

| ステータス | 説明 | 次のアクション |
|-----------|------|---------------|
| 注文受付 | 新規注文 | 処理を開始 |
| 処理中 | 梱包・準備中 | 発送手配 |
| 発送済み | 配送業者に引き渡し | 配達完了を待つ |
| 配達完了 | お客様に到着 | 完了 |
| キャンセル | 注文キャンセル | - |

### 注文のキャンセル

1. 注文詳細ページを開く
2. ステータスを「キャンセル」に変更
3. **重要**: 在庫は自動で戻らないため、手動で在庫を調整

---

## ユーザー管理

### ユーザー一覧の確認

1. 管理画面で「ユーザー」をクリック
2. 登録済みユーザーの一覧を表示

### ユーザー情報の編集

1. ユーザー名をクリック
2. 情報を編集
3. 「保存」をクリック

### パスワードのリセット

管理画面から:
1. ユーザー詳細ページで「このフォームで変更する」リンク
2. 新しいパスワードを入力

コマンドラインから:
```bash
python manage.py changepassword <username>
```

### ユーザーの権限設定

- **スタッフ権限**: 管理画面へのアクセス可能
- **スーパーユーザー権限**: すべての権限

---

## バックアップ

### データベースバックアップ

#### SQLiteの場合（開発環境）

```bash
# データベースファイルをコピー
copy db.sqlite3 backup_db_2025-10-04.sqlite3
```

定期的なバックアップ（推奨: 毎日）:
```bash
# Windowsバッチファイル
@echo off
set TODAY=%date:~0,4%%date:~5,2%%date:~8,2%
copy db.sqlite3 backup\db_%TODAY%.sqlite3
```

#### PostgreSQL/MySQLの場合（本番環境）

PostgreSQL:
```bash
pg_dump -U username dbname > backup_2025-10-04.sql
```

MySQL:
```bash
mysqldump -u username -p dbname > backup_2025-10-04.sql
```

### メディアファイルバックアップ

```bash
# mediaフォルダをコピー
xcopy media backup\media_%TODAY%\ /E /I
```

### バックアップからの復元

SQLite:
```bash
copy backup_db_2025-10-04.sqlite3 db.sqlite3
```

---

## 監視とメンテナンス

### ログの確認

#### アプリケーションログ

開発サーバー起動時のコンソール出力を確認:
- エラーメッセージ
- 警告
- リクエスト/レスポンス情報

#### ログファイルの保存（本番環境推奨）

settings.pyのLOGGING設定でファイル出力を追加:
```python
'handlers': {
    'file': {
        'class': 'logging.FileHandler',
        'filename': 'logs/django.log',
        'formatter': 'verbose',
    },
}
```

### データベースメンテナンス

#### 未使用データの削除

古いセッションの削除:
```bash
python manage.py clearsessions
```

空のカートの削除（カスタムコマンド作成推奨）:
```bash
python manage.py shell
>>> from shop.models import Cart
>>> Cart.objects.filter(items__isnull=True).delete()
```

### パフォーマンス監視

確認項目:
- ページ読み込み時間
- データベースクエリ数
- メモリ使用量

Django Debug Toolbarの使用（開発環境）:
```bash
pip install django-debug-toolbar
```

---

## トラブルシューティング

### 問題: サーバーが起動しない

**原因と対処**:

1. ポートが使用中
   ```bash
   # 別のポートで起動
   python manage.py runserver 8001
   ```

2. マイグレーションが未適用
   ```bash
   python manage.py migrate
   ```

3. 設定ファイルにエラー
   - `config/settings.py`の構文エラーを確認

### 問題: 商品画像が表示されない

**原因と対処**:

1. メディアファイルの設定確認
   ```python
   # settings.py
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```

2. URLパターンの確認
   ```python
   # config/urls.py (DEBUG=Trueの場合)
   from django.conf.urls.static import static
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

3. ファイルパーミッション確認
   ```bash
   # Linuxの場合
   chmod -R 755 media/
   ```

### 問題: ログインできない

**原因と対処**:

1. パスワードを忘れた
   ```bash
   python manage.py changepassword <username>
   ```

2. アカウントが無効化されている
   - 管理画面から「有効」にチェック

3. CSRFエラー
   - ブラウザのキャッシュとCookieをクリア

### 問題: 注文完了後、在庫が減らない

**原因**:
- プログラムのバグまたは処理の中断

**対処**:
1. 注文詳細を確認
2. 手動で在庫を調整
3. ログを確認してエラー原因を特定

### 問題: カートが表示されない

**原因と対処**:

1. セッションが切れた
   - ブラウザを再起動

2. データベースエラー
   ```bash
   python manage.py migrate shop
   ```

3. コンテキストプロセッサの設定確認
   ```python
   # settings.py TEMPLATES
   'context_processors': [
       'shop.context_processors.cart_context',
   ]
   ```

### 問題: 500 Internal Server Error

**対処手順**:

1. DEBUG=Trueにして詳細エラーを確認
   ```python
   # settings.py
   DEBUG = True
   ```

2. ログを確認
   - コンソール出力
   - ログファイル

3. よくあるエラー:
   - データベース接続エラー
   - テンプレートの構文エラー
   - モデルのフィールドエラー

---

## セキュリティチェックリスト

### 本番環境デプロイ前

- [ ] `DEBUG = False`に設定
- [ ] `SECRET_KEY`を環境変数から読み込み
- [ ] `ALLOWED_HOSTS`を設定
- [ ] HTTPS を有効化
- [ ] データベースを本番用（PostgreSQL等）に変更
- [ ] 静的ファイルをCDNから配信
- [ ] バックアップの自動化
- [ ] 定期的なセキュリティアップデート

### 定期的なセキュリティチェック

```bash
# Djangoのセキュリティチェック
python manage.py check --deploy
```

---

## サポート連絡先

### 技術サポート
- Email: support@example.com
- 電話: 03-XXXX-XXXX

### 緊急連絡先
- 24時間サポート: 090-XXXX-XXXX

---

## 更新履歴

| 日付 | バージョン | 変更内容 |
|------|-----------|---------|
| 2025-10-04 | 1.0 | 初版作成 |

---

## 付録

### よく使うDjangoコマンド

```bash
# サーバー起動
python manage.py runserver

# マイグレーション作成
python manage.py makemigrations

# マイグレーション適用
python manage.py migrate

# スーパーユーザー作成
python manage.py createsuperuser

# 静的ファイル収集
python manage.py collectstatic

# キャッシュクリア
python manage.py clear_cache

# Djangoシェル起動
python manage.py shell
```

### データベース操作（Djangoシェル）

```python
# 商品検索
from shop.models import Product
Product.objects.filter(name__icontains="ノート")

# 在庫更新
product = Product.objects.get(id=1)
product.stock = 50
product.save()

# 注文数の集計
from shop.models import Order
Order.objects.filter(status='delivered').count()
```
