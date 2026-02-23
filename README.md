# 上司案件・落とし所AIエージェント

**「今日中に」を今日中にしないAI**

依頼文と自分の状況を入力すると、角の立たない断り・代替案・確認質問・次の一手（返信案）を生成するデモアプリです。

---

## 概要

相手（上司など）の依頼文と、自分の状況を入力すると、AI が返信案を1件生成します。自分の状況は**手動入力**（残り時間・優先度・制約）か**Google Calendar から取得**のいずれかを選べます。ユーザーは返信案をコピーしてメール・チャット等で利用できます。

- **入力**: 依頼文（自由文）、自分の状況の入力元（手動 / Google Calendar）
  - 手動時: 残り時間（数値）、優先度（3段階）、制約（自由文）
  - カレンダー時: 対象日（省略時は今日）— 予定から残り時間・制約を自動導出
- **出力**: 返信案1件（角の立たない断り・代替案・確認質問・次の一手を含む）
- **利用形態**: デモアプリ（認証なし）

---

## AIエージェントの処理フロー

本アプリは、**複数のAIエージェント**を組み合わせて返信案の品質を高めます。

### 処理フロー

自分の状況の入力元が**Google Calendar**の場合は、返信案生成の前に **MCP サーバー（mcp-google）** でスケジュールを取得し、そこから「自分の状況」（残り時間・制約）を導出してから、同じエージェントフローに渡します。

```mermaid
flowchart LR
    subgraph カレンダー取得時
        K[対象日] --> M[MCP サーバー<br/>mcp-google]
        M --> N[Google Calendar API<br/>予定取得]
        N --> O[残り時間・制約の導出]
        O --> P[自分の状況]
    end
```

上記で導出した「自分の状況」を、下図の「依頼文＋自分の状況」として返信案生成エージェントへ渡す。

```mermaid
flowchart TD
    A[依頼文＋自分の状況] --> B[返信案生成エージェント]
    B --> C[返信案リスト 初稿]
    C --> D[返信案チェックエージェント]
    D --> E{チェック結果}
    E -->|OK<br/>全項目8点以上| F[返信案を返却]
    E -->|NG<br/>1項目でも8点未満| G{作り直し回数 < 最大回数?<br/>かつ<br/>スコア合計が改善?}
    G -->|Yes| H[返信案作り直しエージェント]
    H --> I[返信案リスト 修正版]
    I --> D
    G -->|No| F
    
    style B fill:#e1f5ff
    style D fill:#fff4e1
    style H fill:#ffe1f5
    style F fill:#e1ffe1
```

- **カレンダー取得時**: バックエンドが MCP（`MCPServerStdio`）で mcp-google を起動し、`list-calendars` でタスク用カレンダーを特定、`list-events` で対象日の予定を取得。業務時間（9:00–18:00 JST）から予定を差し引いて残り時間を算出し、予定名と時間帯から制約文を組み立て、その「自分の状況」を返信案生成エージェントへ渡す。
- **手動入力時**: ユーザーが入力した残り時間・優先度・制約をそのまま「自分の状況」として返信案生成に渡す。

### エージェントの役割

| エージェント | 役割 | 評価基準 |
|------------|------|---------|
| **返信案生成エージェント** | 依頼文と自分の状況から返信案の初稿を生成 | - |
| **返信案チェックエージェント** | 生成された返信案を3項目で評価（各10点満点） | 1) 角が立っていないか<br>2) 代替案・確認質問が適切か<br>3) 依頼文・制約に反していないか |
| **返信案作り直しエージェント** | チェック結果の指摘（must_fix / nice_to_have）を基に返信案を修正 | - |

### 終了条件

返信案は以下のいずれかの条件で確定します：

1. **チェックがOK**: 3項目すべてが8点以上
2. **最大作り直し回数に達した**: デフォルトは2回まで
3. **スコア合計が改善しない**: 前回と同点または悪化した場合

詳細は [architecture.md](docs/architecture.md) の「3.5 複数エージェントの組み合わせ」を参照してください。

---

## 技術スタック

| 層 | 技術 |
|----|------|
| フロントエンド | React/Next.js |
| バックエンド | Python 3.x, FastAPI |
| AI | PydanticAI + OpenAI（gpt-4o-mini、環境変数で変更可能） |
| 認証 | なし（デモ用途） |

---

## 前提条件

- **Python 3.x** — バックエンド用（[uv](https://docs.astral.sh/uv/) 推奨）
- **Node.js** — フロントエンド用・およびバックエンドの Google Calendar MCP（mcp-google）用（npm / pnpm / yarn のいずれか）
- **OpenAI API キー** — 環境変数で設定（後述）
- **Google Calendar 利用時**: Google Cloud で OAuth 2.0 クライアント ID（デスクトップアプリ）を取得し、環境変数に設定（後述）。初回のみブラウザで認証が必要です。

---

## 起動方法

### クイックスタート（Windows）

プロジェクトルートで `start-dev.ps1` を実行すると、バックエンドとフロントエンドを別ウィンドウで起動します。

```powershell
.\start-dev.ps1
```

- バックエンド: http://localhost:8000
- フロントエンド: http://localhost:3000
- API ドキュメント: http://localhost:8000/docs

> **注意**: バックエンドで AI 生成を使う場合は、バックエンドのウィンドウで `OPENAI_API_KEY` 環境変数を設定してください。

### 手動起動

#### バックエンド（FastAPI）

```bash
cd backend
uv sync
# 環境変数 OPENAI_API_KEY を設定してから
uv run uvicorn settlement_maker.interface.app:app --reload
```

- 依存管理・実行: [uv](https://docs.astral.sh/uv/)（`uv sync`, `uv run ...`）
- テスト: `uv run pytest -q`
- 静的解析: `uv run ruff check .` / `uv run ruff format .` / `uv run mypy .`

#### フロントエンド（Next.js）

```bash
cd frontend
npm install   # または pnpm i / yarn
npm run dev   # Next.js 開発サーバ起動（next dev）
```

- テスト: `npm test`（または `npm run test`）
- lint/format: `npm run lint` / `npm run format`

### 環境変数

#### バックエンド

- **OPENAI_API_KEY** — OpenAI API キー（必須）。環境変数で設定してください。
  ```bash
  # Windows (PowerShell)
  $env:OPENAI_API_KEY = "your-api-key"
  
  # Linux/Mac
  export OPENAI_API_KEY="your-api-key"
  ```
- **OPENAI_MODEL** — 使用する OpenAI モデル（任意、デフォルト: `gpt-5-mini`）
- **GOOGLE_CLIENT_ID** / **GOOGLE_CLIENT_SECRET** — Google Calendar から予定を取得する場合に必要。`.env` に設定すると、MCP（mcp-google）のサブプロセスに渡されます。初回利用時はブラウザで Google アカウントの認証が必要です。

  **MCP 認証で 403: access_denied が出る場合**（主な対処）:
  1. **テストユーザーの追加**（最も多い原因）  
     [Google Cloud Console](https://console.cloud.google.com/) → 「APIとサービス」→「OAuth同意画面」→「テストユーザー」で **認証に使う Google アカウントのメールアドレスを追加**する。アプリが「テスト」の間は、ここに追加したアカウントだけがログインできます。
  2. **OAuth クライアントの種類**  
     「認証情報」で作成したクライアントが **「デスクトップアプリ」** であることを確認する（「ウェブアプリケーション」だと 403 になる場合があります）。
  3. **リダイレクト URI**  
     mcp-google は `http://localhost:3000/oauth2callback` を使うため、デスクトップアプリの場合は通常は自動。問題が続く場合は認証情報の「承認済みのリダイレクト URI」に上記を追加して試す。
  4. **有効な API**  
     「APIとサービス」→「ライブラリ」で **Google Calendar API**（および mcp-google が求める場合は People API 等）が有効か確認する。

#### フロントエンド

- **NEXT_PUBLIC_API_BASE_URL** — バックエンドのベース URL（任意、デフォルト: `http://localhost:8000`）
  - `.env.local` ファイルを作成して設定してください（`.env.local.example` を参考）

### API エンドポイント

- **POST /api/v1/reply-drafts** — 返信案生成
  - リクエスト（共通）: `request_text`（必須）
  - 手動入力時: `situation_source: "manual"`（省略可）、`remaining_hours`, `priority`, `constraints`
  - カレンダー取得時: `situation_source: "calendar"`, `calendar_date`（YYYY-MM-DD、省略時は今日）
  - レスポンス: `{ "draft": { "text": string } }`
  - 詳細は [architecture.md](docs/architecture.md) の「3.3 API 契約」を参照

---

## ドキュメント

仕様・設計・用語は `./docs` で管理しています。

| ドキュメント | 内容 |
|--------------|------|
| [product-requirements.md](docs/product-requirements.md) | プロダクト要求定義書 |
| [functional-design.md](docs/functional-design.md) | 機能設計書 |
| [architecture.md](docs/architecture.md) | 技術仕様書 |
| [repository-structure.md](docs/repository-structure.md) | リポジトリ構造 |
| [development-guidelines.md](docs/development-guidelines.md) | 開発ガイドライン |
| [glossary.md](docs/glossary.md) | 用語定義 |
| [implementation-tasklist.md](docs/implementation-tasklist.md) | 実装タスクリスト（全体進捗） |
| [adr/](docs/adr/) | Architecture Decision Records（ADR） |

- **AI / 開発者向け**: リポジトリルートの [AGENTS.md](AGENTS.md) が最優先ルール（TDD・DDD・ステアリング・契約）です。

---

## ライセンス

（未定。必要に応じて追記してください。）
