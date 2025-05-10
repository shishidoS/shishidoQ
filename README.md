
# SHISHIDOChat プロジェクト

このプロジェクトは、ユーザーが入力した質問をもとに宍戸翔大に関連するプロフィールを抽出し、Google Gemini APIを使用して質問に対する回答を生成するWebアプリケーションです。
ユーザーが質問を入力すると、その内容に関連する人物プロフィールを基に、Gemini AIが自動的に最適な回答を提供します。

## 機能

- ユーザーがメッセージを入力
- Janomeによる形態素解析を使用して、メッセージからキーワードを抽出
- 抽出したキーワードをもとに、関連するプロフィールをデータベースから検索
- Google Gemini APIを使用して、質問に対する回答を生成
- 入力履歴と生成された回答を表示

## 使用技術

- **Django**: Webフレームワークとして使用
- **Janome**: 日本語の形態素解析ライブラリ
- **Google Gemini API**: AIを活用して自然言語での質問に回答
- **SQLite3**: データベースとして使用（Djangoのデフォルト設定）

## インストール方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-username/helpchat.git
cd helpchat
````

### 2. 必要なパッケージのインストール

Python 3.x がインストールされていることを前提に、仮想環境をセットアップします。

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

必要なパッケージをインストールします。

```bash
pip install -r requirements.txt
```

### 3. 設定ファイルの編集

Google Gemini APIを使用するために、`YOUR_GEMINI_API_KEY`にあなたのAPIキーを設定してください。

```python
os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
```

### 4. マイグレーションの実行

データベースの初期化を行います。

```bash
python manage.py migrate
```

### 5. 開発用サーバの起動

以下のコマンドで開発用サーバを起動します。

```bash
python manage.py runserver
```

その後、ブラウザで [http://127.0.0.1:8000/](http://127.0.0.1:8000/) にアクセスして、アプリケーションを使用できます。

## 使い方

1. メッセージ欄に質問を入力し、「送信」ボタンをクリックします。
2. アプリケーションが自動的に質問内容を解析し、関連するプロフィールをデータベースから検索します。
3. Google Gemini APIを使って、最適な回答が生成され、画面に表示されます。

## ファイル構成

* `helpchat/`: プロジェクト全体

  * `inputapp/`: アプリケーションのメインロジック

    * `models.py`: データベースモデル（`Profile`, `Inquiry`）
    * `views.py`: ビュー関数（`input_view`, `result_view`）
    * `forms.py`: フォームクラス（`InquiryForm`）
    * `templates/`: HTMLテンプレート
    * `static/`: 静的ファイル（CSS, JS）
  * `requirements.txt`: 必要なパッケージ
  * `settings.py`: Django設定ファイル
  * `urls.py`: URL設定

## 注意事項

* Google Gemini APIのキーが無効な場合、APIからの応答が得られません。APIキーが正しいことを確認してください。
* Janomeによる形態素解析が正常に動作しない場合、必要な辞書が不足している可能性があります。`mecab`や`ipadic`のインストールを確認してください。

## 開発者向け

このプロジェクトはDjangoベースであり、以下のコマンドで開発を行うことができます。

### テストの実行

```bash
python manage.py test
```

### 管理者アカウントの作成

Djangoの管理画面にアクセスするためのアカウントを作成します。

```bash
python manage.py createsuperuser
```

その後、[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) から管理画面にアクセスできます。

## ライセンス

MIT License (MIT)

```

### このテンプレートの使い方

1. プロジェクトの詳細に応じて、`YOUR_GEMINI_API_KEY`の部分に実際のAPIキーを設定してください。
2. 必要なパッケージを`requirements.txt`に記載し、依存関係を管理してください。
3. プロジェクトに合わせて説明を更新し、ファイル構成や使い方を適切に変更します。

この`README.md`がプロジェクトのセットアップと使用方法をわかりやすく説明するための一助になるはずです。
```
