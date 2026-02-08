# 上司案件・落とし所AIエージェント

**「今日中に」を今日中にしないAI**

依頼文と自分の状況を入力すると、角の立たない断り・代替案・確認質問・次の一手（返信案）を生成するデモアプリです。

---

## 概要

相手（上司など）の依頼文と、自分の状況（残り時間・優先度・制約）を入力すると、AI が複数の返信案を生成します。ユーザーは返信案を一覧で選び、コピーしてメール・チャット等で利用できます。

- **入力**: 依頼文（自由文）、残り時間（数値）、優先度（3段階）、制約（自由文）
- **出力**: 複数の返信案（角の立たない断り・代替案・確認質問・次の一手を含む）
- **利用形態**: デモアプリ（認証なし）

---

## 技術スタック

| 層 | 技術 |
|----|------|
| フロントエンド | React/Next.js |
| バックエンド | Python 3.x, FastAPI |
| AI | PydanticAI + OpenAI（gpt-5-mini または同等モデル） |
| 認証 | なし（デモ用途） |

---

## 前提条件

- **Python 3.x** — バックエンド用（[uv](https://docs.astral.sh/uv/) 推奨）
- **Node.js** — フロントエンド用（npm / pnpm / yarn のいずれか）
- **OpenAI API キー** — 環境変数で設定（後述）

---

## 起動方法

> 現時点ではバックエンド・フロントエンドは未実装です。以下の手順は実装完了後の想定です。

### バックエンド（FastAPI）

```bash
cd backend
uv sync
# 環境変数 OPENAI_API_KEY を設定してから
uv run uvicorn settlement_maker.interface.app:app --reload
```

- 依存管理・実行: [uv](https://docs.astral.sh/uv/)（`uv sync`, `uv run ...`）
- テスト: `uv run pytest -q`
- 静的解析: `uv run ruff check .` / `uv run ruff format .` / `uv run mypy .`

### フロントエンド（Next.js）

```bash
cd frontend
npm install   # または pnpm i / yarn
npm run dev   # Next.js 開発サーバ起動（next dev）
```

- テスト: `npm test`（または `npm run test`）
- lint/format: `npm run lint` / `npm run format`

### 環境変数

- **OPENAI_API_KEY** — OpenAI API キー（バックエンドで使用）。コードに埋め込まず、環境変数で渡してください。

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
